from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session 
from sqlalchemy import and_, cast, Date
from .models import db, Complaint, Repair, User, ResourceManpower, ResourceMachine, ResourceMaterial, BranchOffice, RepairMachineAllocation, RepairManpowerAllocation, RepairMaterialAllocation
from .forms import RepairForm, UpdateRepairCalenderDate
import datetime
from .auth import auth_bp

supervisor_bp = Blueprint('supervisor', __name__)

# ---------------------------------------------
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

# ---------------------------------------------
@supervisor_bp.route('/recived_complaints_list', methods=['GET'])
def home_page():
    user_branch_office_id = verify_login()
    unaccepted_complaints = db.session.query(Complaint).filter(Complaint.status == 'Unaccepted').all()
    accepted_complaints = db.session.query(Complaint).filter(Complaint.status == 'Accepted').all()
    return render_template("supervisor/supervisor.html", unaccepted_complaints=unaccepted_complaints, accepted_complaints=accepted_complaints)

# ---------------------------------------------
@supervisor_bp.route('/available_resources', methods=['GET'])
def available_resources():
    verify_login()
    today = datetime.date.today()
    
    ongoing_repairs = db.session.query(Repair).filter(Repair.status.in_(['In Progress'])).all()
    if not ongoing_repairs:
        flash("No ongoing repairs found", "info")

    for repair in ongoing_repairs:
        # Machine
        for machine in RepairMachineAllocation.query.filter_by(repair_id=repair.id):
            machine_obj = ResourceMachine.query.get(machine.machine_id)
            machine_obj.in_use = machine.quantity_allocated
            db.session.add(machine_obj)

        # Manpower
        for manpower in RepairManpowerAllocation.query.filter_by(repair_id=repair.id):
            manpower_obj = ResourceManpower.query.get(manpower.manpower_id)
            manpower_obj.in_use = manpower.quantity_allocated
            db.session.add(manpower_obj)

        # --- MATERIAL SUPPORT ---
        for material in RepairMaterialAllocation.query.filter_by(repair_id=repair.id):
            material_obj = ResourceMaterial.query.get(material.material_id)
            material_obj.in_use = material.quantity_allocated
            db.session.add(material_obj)

    db.session.commit()

    return render_template(
        'supervisor/available_resources.html',
        machines=ResourceMachine.query.all(),
        manpower=ResourceManpower.query.all(),
        materials=ResourceMaterial.query.all()
    )

# ---------------------------------------------
@supervisor_bp.route('/calendar', methods=['GET', 'POST'])
def view_calendar():
    form = UpdateRepairCalenderDate()
    if request.method == 'POST' and form.validate_on_submit():
        repair = Repair.query.get(form.repair_id.data)
        repair.start_date = form.start_date.data
        repair.expected_completion_date = form.expected_completion_date.data
        db.session.commit()
        flash("Repair dates updated successfully", "success")
        return redirect(url_for('supervisor.view_calendar'))

    repairs = Repair.query.filter(Repair.status.in_(['Scheduled', 'In Progress'])).all()
    return render_template('supervisor/calendar.html', repair_form=form, repairs=repairs)

# ---------------------------------------------
@supervisor_bp.route('/assign_repair/<int:complaint_id>', methods=['GET', 'POST'])
def assign_repair(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    form = RepairForm()

    existing_repair = Repair.query.filter_by(complaint_id=complaint.id).first()
    existing_machine_allocs = RepairMachineAllocation.query.filter_by(repair_id=existing_repair.id).all() if existing_repair else []
    existing_manpower_allocs = RepairManpowerAllocation.query.filter_by(repair_id=existing_repair.id).all() if existing_repair else []
    existing_material_allocs = RepairMaterialAllocation.query.filter_by(repair_id=existing_repair.id).all() if existing_repair else []

    machine_alloc_map = {alloc.machine_id: alloc for alloc in existing_machine_allocs}
    manpower_alloc_map = {alloc.manpower_id: alloc for alloc in existing_manpower_allocs}
    material_alloc_map = {alloc.material_id: alloc for alloc in existing_material_allocs}

    if existing_repair and request.method == 'GET':
        form.process(obj=existing_repair)

    if form.validate_on_submit():
        if existing_repair:
            existing_repair.priority = form.priority.data
            existing_repair.days_to_complete = form.days_to_complete.data
            RepairMachineAllocation.query.filter_by(repair_id=existing_repair.id).delete()
            RepairManpowerAllocation.query.filter_by(repair_id=existing_repair.id).delete()
            RepairMaterialAllocation.query.filter_by(repair_id=existing_repair.id).delete()
            repair = existing_repair
        else:
            repair = Repair(
                complaint_id=complaint.id,
                supervisor_id=session["user_id"],
                priority=form.priority.data,
                status='Unscheduled',
                days_to_complete=form.days_to_complete.data,
                start_date=None,
                expected_completion_date=None,
                completion_date=None
            )
            db.session.add(repair)
            db.session.flush()

        # Machines
        for machine_id, qty in zip(request.form.getlist('machine_ids[]'), request.form.getlist('machine_quantities[]')):
            machine_id, qty = int(machine_id), int(qty)
            machine = ResourceMachine.query.get(machine_id)
            machine.currently_requested += qty
            db.session.add(machine)
            db.session.add(RepairMachineAllocation(repair_id=repair.id, machine_id=machine_id, quantity_allocated=0, quantity_requested=qty))

        # Manpower
        for mp_id, qty in zip(request.form.getlist('manpower_ids[]'), request.form.getlist('manpower_quantities[]')):
            mp_id, qty = int(mp_id), int(qty)
            manpower = ResourceManpower.query.get(mp_id)
            manpower.currently_requested += qty
            db.session.add(manpower)
            db.session.add(RepairManpowerAllocation(repair_id=repair.id, manpower_id=mp_id, quantity_allocated=0, quantity_requested=qty))

        # --- MATERIAL SUPPORT ---
        for mat_id, qty in zip(request.form.getlist('material_ids[]'), request.form.getlist('material_quantities[]')):
            mat_id, qty = int(mat_id), float(qty)
            material = ResourceMaterial.query.get(mat_id)
            material.currently_requested += qty
            db.session.add(material)
            db.session.add(RepairMaterialAllocation(repair_id=repair.id, material_id=mat_id, quantity_allocated=0, quantity_requested=qty))

        repair.status = 'Unscheduled'
        complaint.status = 'Accepted'

        db.session.add(complaint)
        db.session.add(repair)
        db.session.commit()

        flash("Repair updated successfully" if existing_repair else "Repair created and resources requested", "success")
        return redirect(url_for('supervisor.home_page'))

    return render_template(
        'supervisor/assign_repair.html',
        form=form,
        complaint=complaint,
        machines=ResourceMachine.query.all(),
        manpower=ResourceManpower.query.all(),
        materials=ResourceMaterial.query.all(),  # <--- New
        existing_repair=existing_repair,
        machine_alloc_map=machine_alloc_map,
        manpower_alloc_map=manpower_alloc_map,
        material_alloc_map=material_alloc_map  # <--- New
    )

# ---------------------------------------------
@supervisor_bp.route('/all_repairs')
def view_repair():
    all_repairs = db.session.query(Repair).filter(Repair.supervisor_id == session["user_id"]).all()
    for r in all_repairs:
        r.start_date = r.start_date.strftime("%Y-%m-%d") if r.start_date else None
        r.expected_completion_date = r.expected_completion_date.strftime("%Y-%m-%d") if r.expected_completion_date else None
        r.completion_date = r.completion_date.strftime("%Y-%m-%d") if r.completion_date else None
    return render_template('supervisor/all_repairs.html', all_repairs=all_repairs)

# ---------------------------------------------
@supervisor_bp.route('/r/mark_complete/repair/<int:repair_id>', methods=['GET'])
def mark_complete(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    repair.status = 'Completed'
    repair.completion_date = datetime.date.today()
    Complaint.query.filter_by(id=repair.complaint_id).update({"status": "Completed"})

    # Machines
    for machine in RepairMachineAllocation.query.filter_by(repair_id=repair_id).all():
        m_obj = ResourceMachine.query.get(machine.machine_id)
        m_obj.currently_allocated -= machine.quantity_allocated
        m_obj.in_use = 0
        db.session.add(m_obj)

    # Manpower
    for mp in RepairManpowerAllocation.query.filter_by(repair_id=repair_id).all():
        mp_obj = ResourceManpower.query.get(mp.manpower_id)
        mp_obj.currently_allocated -= mp.quantity_allocated
        mp_obj.in_use = 0
        db.session.add(mp_obj)

    # --- MATERIAL SUPPORT ---
    for mat in RepairMaterialAllocation.query.filter_by(repair_id=repair_id).all():
        mat_obj = ResourceMaterial.query.get(mat.material_id)
        mat_obj.currently_allocated -= mat.quantity_allocated
        mat_obj.in_use = 0
        db.session.add(mat_obj)

    db.session.commit()
    flash("Repair marked as completed", "success")
    return redirect(url_for('supervisor.view_repair'))
