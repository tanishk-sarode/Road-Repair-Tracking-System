import logging
import random
import datetime
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from .models import (
    db, Complaint, Repair, User,
    ResourceManpower, ResourceMachine, ResourceMaterial,
    RepairSchedule,
    RepairMachineAllocation, RepairManpowerAllocation, RepairMaterialAllocation
)
from .supervisor_routes import verify_login as verify_login_supervisor
from .auth import auth_bp

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    user_type = session.get("user_type")
    logging.info(f"Accessing home route. User type: {user_type}")

    if not user_type:
        flash("Access denied. Please log in to continue.", "danger")
        return redirect(url_for("auth.login"))

    if user_type == "admin":
        return render_template('admin.html')
    elif user_type == "supervisor":
        return redirect(url_for('supervisor.home_page'))
    elif user_type == "resident":
        return redirect(url_for("resident.home_page"))
    elif user_type == "clerk":
        return redirect(url_for("clerk.home_page"))
    elif user_type == "mayor":
        return render_template('mayor.html')

    flash("Invalid user type. Please contact support.", "warning")
    return redirect(url_for("auth.login"))

def generate_random_color():
    return f'#{random.randint(0, 0xFFFFFF):06x}'

@main_bp.route('/repair_events')
def repair_events():
    repairs = Repair.query.filter(Repair.status.in_(['Scheduled', 'In Progress'])).all()
    events = []

    for r in repairs:
        color = generate_random_color()
        if r.start_date:
            events.append({
                "id": f"start-{r.id}",
                "title": f"Start: Repair #{r.id}",
                "start": r.start_date.date().isoformat(),
                "end": (r.start_date.date() + datetime.timedelta(days=1)).isoformat(),
                "color": color,
                "allDay": True
            })
        if r.expected_completion_date:
            events.append({
                "id": f"end-{r.id}",
                "title": f"End: Repair #{r.id}",
                "start": r.expected_completion_date.date().isoformat(),
                "end": (r.expected_completion_date.date() + datetime.timedelta(days=1)).isoformat(),
                "color": color,
                "allDay": True
            })
    return jsonify(events)

@main_bp.route('/schedule_repairs')
def schedule_repairs():
    today = datetime.date.today()
    max_start_window = today + datetime.timedelta(days=45)

    repairs = Repair.query.filter(Repair.status.in_(['Unscheduled', "Accepted"])).order_by(Repair.priority.desc()).all()
    if not repairs:
        flash("No repairs found.")

    machine_avail = {m.id: [0] * 46 for m in ResourceMachine.query.all()}
    manpower_avail = {m.id: [0] * 46 for m in ResourceManpower.query.all()}
    material_avail = {m.id: [0] * 46 for m in ResourceMaterial.query.all()}

    existing_repairs = Repair.query.filter(Repair.status.in_(['Scheduled', 'In Progress'])).all()
    for rep in existing_repairs:
        if rep.start_date is None or rep.expected_completion_date is None:
            continue

        days = (rep.expected_completion_date - rep.start_date).days
        start_offset = max((rep.start_date.date() - today).days, 0)

        for alloc in RepairMachineAllocation.query.filter_by(repair_id=rep.id):
            for d in range(start_offset, min(46, start_offset + days)):
                machine_avail[alloc.machine_id][d] += alloc.quantity_allocated

        for alloc in RepairManpowerAllocation.query.filter_by(repair_id=rep.id):
            for d in range(start_offset, min(46, start_offset + days)):
                manpower_avail[alloc.manpower_id][d] += alloc.quantity_allocated

        for alloc in RepairMaterialAllocation.query.filter_by(repair_id=rep.id):
            for d in range(start_offset, min(46, start_offset + days)):
                material_avail[alloc.material_id][d] += alloc.quantity_allocated

    for repair in repairs:
        machine_allocs = RepairMachineAllocation.query.filter_by(repair_id=repair.id).all()
        manpower_allocs = RepairManpowerAllocation.query.filter_by(repair_id=repair.id).all()
        material_allocs = RepairMaterialAllocation.query.filter_by(repair_id=repair.id).all()
        days_required = repair.days_to_complete

        scheduled = False
        for day_offset in range(0, 46 - days_required + 1):
            can_allocate = True

            for alloc in machine_allocs:
                needed = alloc.quantity_requested
                for d in range(day_offset, day_offset + days_required):
                    available = ResourceMachine.query.get(alloc.machine_id).total_available - machine_avail[alloc.machine_id][d]
                    if available < needed:
                        can_allocate = False
                        break
                if not can_allocate:
                    break

            for alloc in manpower_allocs:
                needed = alloc.quantity_requested
                for d in range(day_offset, day_offset + days_required):
                    available = ResourceManpower.query.get(alloc.manpower_id).total_available - manpower_avail[alloc.manpower_id][d]
                    if available < needed:
                        can_allocate = False
                        break
                if not can_allocate:
                    break

            for alloc in material_allocs:
                needed = alloc.quantity_requested
                for d in range(day_offset, day_offset + days_required):
                    available = ResourceMaterial.query.get(alloc.material_id).total_available - material_avail[alloc.material_id][d]
                    if available < needed:
                        can_allocate = False
                        break
                if not can_allocate:
                    break

            if can_allocate:
                for alloc in machine_allocs:
                    alloc.quantity_allocated += alloc.quantity_requested
                    alloc.quantity_requested = 0
                    for d in range(day_offset, day_offset + days_required):
                        machine_avail[alloc.machine_id][d] += alloc.quantity_allocated
                    db.session.add(alloc)
                    res_machine = ResourceMachine.query.get(alloc.machine_id)
                    res_machine.currently_allocated += alloc.quantity_allocated
                    res_machine.currently_requested = max(res_machine.currently_requested - alloc.quantity_allocated, 0)
                    db.session.add(res_machine)

                for alloc in manpower_allocs:
                    alloc.quantity_allocated += alloc.quantity_requested
                    alloc.quantity_requested = 0
                    for d in range(day_offset, day_offset + days_required):
                        manpower_avail[alloc.manpower_id][d] += alloc.quantity_allocated
                    db.session.add(alloc)
                    res_manpower = ResourceManpower.query.get(alloc.manpower_id)
                    res_manpower.currently_allocated += alloc.quantity_allocated
                    res_manpower.currently_requested = max(res_manpower.currently_requested - alloc.quantity_allocated, 0)
                    db.session.add(res_manpower)


                for alloc in material_allocs:
                    alloc.quantity_allocated += alloc.quantity_requested
                    alloc.quantity_requested = 0
                    for d in range(day_offset, day_offset + days_required):
                        material_avail[alloc.material_id][d] += alloc.quantity_allocated
                    db.session.add(alloc)
                    res_material = ResourceMaterial.query.get(alloc.material_id)
                    res_material.currently_allocated += alloc.quantity_allocated
                    res_material.currently_requested = max(res_material.currently_requested - alloc.quantity_allocated, 0)
                    db.session.add(res_material)


                repair.start_date = today + datetime.timedelta(days=day_offset)
                repair.expected_completion_date = repair.start_date + datetime.timedelta(days=days_required)
                # Add or update RepairSchedule
                
                existing_schedule = RepairSchedule.query.filter_by(repair_id=repair.id).first()
                if not existing_schedule:
                    schedule = RepairSchedule(
                        repair_id=repair.id,
                        start_date=repair.start_date,
                        end_date=repair.expected_completion_date,
                        status=repair.status
                    )
                    db.session.add(schedule)
                else:
                    existing_schedule.start_date = repair.start_date
                    existing_schedule.end_date = repair.expected_completion_date
                    existing_schedule.status = repair.status
                    db.session.add(existing_schedule)

                if repair.start_date == today:
                    Complaint.query.filter_by(id=repair.complaint_id).update({"status": "In Progress"})
                    repair.status = 'In Progress'
                else:
                    repair.status = 'Scheduled'
                complaint = Complaint.query.get(repair.complaint_id)
                if complaint:
                    complaint.status = "In Progress"
                    db.session.add(complaint)

                db.session.add(repair)
                scheduled = True
                break

        if not scheduled:
            repair.status = 'Unscheduled'
            db.session.add(repair)

    db.session.commit()
    flash("Repair scheduling complete based on resource timelines.", "info")
    return redirect(url_for('supervisor.home_page'))

@main_bp.route('/repair_details/<int:repair_id>', methods=['GET'])
def repair_details(repair_id):
    print(f"Fetching details for Repair ID: {repair_id}")

    repair = Repair.query.get_or_404(repair_id)
    complaint = Complaint.query.get(repair.complaint_id)
    resident = User.query.get(complaint.residence_id)
    machines = RepairMachineAllocation.query.filter_by(repair_id=repair_id).all()
    manpower = RepairManpowerAllocation.query.filter_by(repair_id=repair_id).all()
    materials = RepairMaterialAllocation.query.filter_by(repair_id=repair_id).all()

    machine_list = [f"Machine ID: {m.machine_id}, Quantity: {m.quantity_allocated}" for m in machines]
    manpower_list = [f"Manpower ID: {m.manpower_id}, Quantity: {m.quantity_allocated}" for m in manpower]
    material_list = [f"Material ID: {m.material_id}, Quantity: {m.quantity_allocated}" for m in materials]

    return jsonify({
        'id': repair.id,
        'description': complaint.description,
        'location': complaint.location,
        'status': repair.status,
        'start_date': repair.start_date.strftime('%Y-%m-%d') if repair.start_date else "N/A",
        'end_date': repair.expected_completion_date.strftime('%Y-%m-%d') if repair.expected_completion_date else "N/A",
        'machines': ', '.join(machine_list),
        'manpower': ', '.join(manpower_list),
        'materials': ', '.join(material_list)
    })
