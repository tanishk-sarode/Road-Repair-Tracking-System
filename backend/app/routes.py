import logging  # Add logging for debugging
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Complaint, Repair, User, ResourceManpower, ResourceMachine, RepairSchedule, RepairMachineAllocation, RepairManpowerAllocation
from .supervisor_routes import verify_login as verify_login_supervisor
import datetime
from .auth import auth_bp

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    user_type = session.get("user_type")  # Fetch user role from session
    logging.info(f"Accessing home route. User type: {user_type}")  # Log user type

    if not user_type:
        flash("Access denied. Please log in to continue.", "danger")
        return redirect(url_for("auth.login"))  # Redirect to login page

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


import random

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
        print("No repairs found.")
    
    # Cache available resources
    machine_avail = {machine.id: [0] * 46 for machine in ResourceMachine.query.all()}
    manpower_avail = {manpower.id: [0] * 46 for manpower in ResourceManpower.query.all()}

    # Fetch existing scheduled/in-progress repairs
    existing_repairs = Repair.query.filter(Repair.status.in_(['Scheduled', 'In Progress'])).all()

    for rep in existing_repairs:
        if rep.start_date is None or rep.expected_completion_date is None:
            continue  # Avoid crash if some dates are NULL

        days = (rep.expected_completion_date - rep.start_date).days
        start_offset = max((rep.start_date.date() - today).days, 0)

        for alloc in RepairMachineAllocation.query.filter_by(repair_id=rep.id):
            for d in range(start_offset, min(46, start_offset + days)):
                machine_avail[alloc.machine_id][d] += alloc.quantity_allocated

        for alloc in RepairManpowerAllocation.query.filter_by(repair_id=rep.id):
            for d in range(start_offset, min(46, start_offset + days)):
                manpower_avail[alloc.manpower_id][d] += alloc.quantity_allocated

    # Schedule new repairs
    for repair in repairs:
        machine_allocs = RepairMachineAllocation.query.filter_by(repair_id=repair.id).all()
        manpower_allocs = RepairManpowerAllocation.query.filter_by(repair_id=repair.id).all()
        days_required = repair.days_to_complete

        scheduled = False
        for day_offset in range(0, 46 - days_required + 1):
            can_allocate = True

            # Check machine availability
            for alloc in machine_allocs:
                needed = alloc.quantity_requested
                for d in range(day_offset, day_offset + days_required):
                    available = ResourceMachine.query.get(alloc.machine_id).total_available - machine_avail[alloc.machine_id][d]
                    if available < needed:
                        can_allocate = False
                        break
                if not can_allocate:
                    break

            # Check manpower availability
            for alloc in manpower_allocs:
                needed = alloc.quantity_requested
                for d in range(day_offset, day_offset + days_required):
                    available = ResourceManpower.query.get(alloc.manpower_id).total_available - manpower_avail[alloc.manpower_id][d]
                    if available < needed:
                        can_allocate = False
                        break
                if not can_allocate:
                    break

            if can_allocate:
                # Allocate machines and manpower
                for alloc in machine_allocs:
                    alloc.quantity_allocated += alloc.quantity_requested
                    alloc.quantity_requested = 0
                    for d in range(day_offset, day_offset + days_required):
                        machine_avail[alloc.machine_id][d] += alloc.quantity_allocated
                    db.session.add(alloc)

                for alloc in manpower_allocs:
                    alloc.quantity_allocated += alloc.quantity_requested
                    alloc.quantity_requested = 0
                    for d in range(day_offset, day_offset + days_required):
                        manpower_avail[alloc.manpower_id][d] += alloc.quantity_allocated
                    db.session.add(alloc)

                repair.start_date = today + datetime.timedelta(days=day_offset)
                repair.expected_completion_date = repair.start_date + datetime.timedelta(days=days_required)
                if repair.start_date == today:
                    Complaint.query.filter_by(id=repair.complaint_id).update({"status": "In Progress"})
                    repair.status = 'In Progress'
                else:
                    repair.status = 'Scheduled'
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

    print(f"Fetching details for Repair ID: {repair_id}")  # Add this line for debugging
    
    repair = Repair.query.get_or_404(repair_id)
    complaint = Complaint.query.get(repair.complaint_id)
    resident = User.query.get(complaint.residence_id)
    machines = RepairMachineAllocation.query.filter_by(repair_id=repair_id).all()
    manpower = RepairManpowerAllocation.query.filter_by(repair_id=repair_id).all()
    
    # Format data for the modal
    machine_list = [f"Machine ID: {m.machine_id}, Quantity: {m.quantity_allocated}" for m in machines]
    manpower_list = [f"Manpower ID: {m.manpower_id}, Quantity: {m.quantity_allocated}" for m in manpower]
    
    x= jsonify({
        'id': repair.id,
        'description': complaint.description,
        'location': complaint.location,
        'status': repair.status,
        'start_date': repair.start_date.strftime('%Y-%m-%d'),
        'end_date': repair.expected_completion_date.strftime('%Y-%m-%d'),
        'machines': ', '.join(machine_list),
        'manpower': ', '.join(manpower_list)
    })
    print(x)
    return x


