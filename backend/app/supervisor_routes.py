from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session 
from sqlalchemy import and_, cast, Date
from .models import db, Complaint, Repair, User, ResourceManpower, ResourceMachine, BranchOffice,RepairMachineAllocation, RepairManpowerAllocation
from .forms import  RepairForm, UpdateRepairCalender
import datetime
from .auth import auth_bp

supervisor_bp = Blueprint('supervisor', __name__)

def verify_login():
    if "user_id" not in session:
        flash("You need to log in first!", "warning")
        return redirect(url_for("main.login"))
    if session["user_type"] != "supervisor":    
        flash("You are not authorized to access this page!", "danger")
        return redirect(url_for("main.home"))
    user_branch_office_id = db.session.query(BranchOffice).filter_by(supervisor_id=session["user_id"]).first().id
    if user_branch_office_id is None:
        flash("You are not authorized to access this page!", "danger")
        return redirect(url_for("main.home"))
    return user_branch_office_id

@supervisor_bp.route('/recived_complaints_list', methods=['GET'])
def home_page():
    user_branch_office_id = verify_login()
    unaccepted_complaints = db.session.query(Complaint).filter(Complaint.status == 'Unaccepted').all()
    accepted_complaints = db.session.query(Complaint).filter(Complaint.status == 'Accepted').all()
    # return jsonify(complaints=complaints_list)
    return render_template("supervisor/supervisor.html", unaccepted_complaints=unaccepted_complaints, accepted_complaints=accepted_complaints)



@supervisor_bp.route('/available_resources', methods=['GET'])
def available_resources():
    verify_login()
    today = datetime.date.today()
    
    ongoing_repairs = db.session.query(Repair).filter(Repair.status.in_(['In Progress'])).all()
    if not ongoing_repairs:
        flash("No ongoing repairs found", "info")

    for repair in ongoing_repairs:
        machines_in_use = RepairMachineAllocation.query.filter_by(repair_id=repair.id).all()
        for machine in machines_in_use:
            machine_obj = ResourceMachine.query.get(machine.machine_id)
            machine_obj.in_use = machine.quantity_allocated  # Use quantity_allocated from the allocation
            print("Machine in use:", machine_obj.name)
            db.session.add(machine_obj)

        manpower_in_use = RepairManpowerAllocation.query.filter_by(repair_id=repair.id).all()
        for manpower in manpower_in_use:
            manpower_obj = ResourceManpower.query.get(manpower.manpower_id)
            manpower_obj.in_use = manpower.quantity_allocated  # Use quantity_allocated here too
            print("Manpower in use:", manpower_obj.role)
            db.session.add(manpower_obj)

    db.session.commit()

    machines = ResourceMachine.query.all()
    manpower = ResourceManpower.query.all()
    
    return render_template('supervisor/available_resources.html', machines=machines, manpower=manpower)

@supervisor_bp.route('/calendar', methods=['GET', 'POST'])
def view_calendar():
    form=UpdateRepairCalender()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            print("FORM DATA:", request.form)  # 👈 add this
            repair = Repair.query.get(form.repair_id.data)
            repair.start_date = form.start_date.data
            repair.expected_completion_date = form.expected_completion_date.data
            db.session.commit()
            flash("Repair dates updated successfully", "success")
            return redirect(url_for('supervisor.view_calendar'))    
        else:
            flash("Invalid form submission", "danger")
            print("FORM DATA:", request.form)
            print("FORM ERRORS:", form.errors)
            return redirect(url_for('supervisor.view_calendar'))
    repairs = Repair.query.filter(Repair.status.in_(['Scheduled', 'In Progress'])).all()
    return render_template('supervisor/calendar.html', repair_form=form, repairs=repairs)


@supervisor_bp.route('/assign_repair/<int:complaint_id>', methods=['GET', 'POST'])
def assign_repair(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    form = RepairForm()

    if form.validate_on_submit():
        schedule_machine, schedule_manpower = True, True

        repair = Repair(
            complaint_id=complaint.id,
            supervisor_id=session["user_id"],
            priority=form.priority.data,
            status='Unscheduled',  # Default status
            days_to_complete=form.days_to_complete.data,
            start_date=None,
            expected_completion_date=None,
            completion_date=None
        )
        db.session.add(repair)
        db.session.flush()

        machine_ids = request.form.getlist('machine_ids[]')
        machine_quantities = request.form.getlist('machine_quantities[]')
        manpower_ids = request.form.getlist('manpower_ids[]')
        manpower_quantities = request.form.getlist('manpower_quantities[]')

        # Only request (not allocate) machines
        for machine_id, qty in zip(machine_ids, machine_quantities):
            qty = int(qty)
            machine_id = int(machine_id)
            machine = ResourceMachine.query.get(machine_id)

            available_qty = machine.total_available - machine.currently_allocated

            if qty > available_qty:
                schedule_machine = False
                machine.currently_requested += qty - available_qty

            db.session.add(machine)
            db.session.add(RepairMachineAllocation(
                repair_id=repair.id,
                machine_id=machine_id,
                quantity_allocated=0,  # No allocation yet
                quantity_requested=qty
            ))

        # Only request (not allocate) manpower
        for mp_id, qty in zip(manpower_ids, manpower_quantities):
            qty = int(qty)
            mp_id = int(mp_id)
            manpower = ResourceManpower.query.get(mp_id)

            available_qty = manpower.total_available - manpower.currently_allocated

            if qty > available_qty:
                schedule_manpower = False
                manpower.currently_requested += qty - available_qty

            db.session.add(manpower)
            db.session.add(RepairManpowerAllocation(
                repair_id=repair.id,
                manpower_id=mp_id,
                quantity_allocated=0,
                quantity_requested=qty
            ))

        # Final status
        repair.status = 'Unscheduled'
        complaint.status = 'Accepted'

        db.session.add(complaint)
        db.session.add(repair)
        db.session.commit()

        flash("Repair created and resources requested", "success")
        return redirect(url_for('supervisor.home_page'))

    return render_template(
        'supervisor/assign_repair.html',
        form=form,
        complaint=complaint,
        machines=ResourceMachine.query.all(),
        manpower=ResourceManpower.query.all()
    )

@supervisor_bp.route('/all_repairs')
def view_repair():
    all_repairs = db.session.query(Repair).filter(Repair.supervisor_id == session["user_id"]).all()
    for repairs in all_repairs:
        repairs.start_date = repairs.start_date.strftime("%Y-%m-%d") if repairs.start_date else None
        repairs.expected_completion_date = repairs.expected_completion_date.strftime("%Y-%m-%d") if repairs.expected_completion_date else None
        repairs.completion_date = repairs.completion_date.strftime("%Y-%m-%d") if repairs.completion_date else None
    return render_template('supervisor/all_repairs.html', all_repairs=all_repairs)

@supervisor_bp.route('r/mark_complete/repair/<int:repair_id>', methods=['GET'])
def mark_complete(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    repair.status = 'Completed'
    repair.completion_date = datetime.date.today()
    Complaint.query.filter_by(id=repair.complaint_id).update({
        "status": "Completed",
    })
    machines = RepairMachineAllocation.query.filter_by(repair_id=repair_id).all()
    for machine in machines:
        machine_obj = ResourceMachine.query.get(machine.machine_id)
        machine_obj.currently_allocated -= machine.quantity_allocated
        machine_obj.in_use = 0
        db.session.add(machine_obj)
    manpower = RepairManpowerAllocation.query.filter_by(repair_id=repair_id).all()
    for manpower in manpower:
        manpower_obj = ResourceManpower.query.get(manpower.manpower_id)
        manpower_obj.currently_allocated -= manpower.quantity_allocated
        manpower_obj.in_use = 0
        db.session.add(manpower_obj)
    
    db.session.commit()
    flash("Repair marked as completed", "success")
    return redirect(url_for('supervisor.view_repair'))