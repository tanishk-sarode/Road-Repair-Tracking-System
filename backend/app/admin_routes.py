from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required
from . import db
from .models import (
    RepairMachineAllocation, RepairMaterialAllocation, RepairManpowerAllocation, 
    Repair, Complaint, ResourceMachine, ResourceMaterial, ResourceManpower
)
from .forms import RepairForm, MachineForm, ManpowerForm, MaterialForm, MaterialAllocationForm

# Use consistent naming for models
Machine = ResourceMachine
Manpower = ResourceManpower
Material = ResourceMaterial

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- Resource Management Routes ---
def verify_login():
    if "user_id" not in session:
        flash("You need to log in first!", "warning")
        return redirect(url_for("main.login"))
    if ("admin" or "administrator") not in session["user_type"]:    
        flash("You are not authorized to access this page!", "danger")
        return redirect(url_for("main.home"))
    return True

# Machine Management
@admin_bp.route('/machines', methods=['GET', 'POST'])
def manage_machines():
    verify_login()
    form = MachineForm()
    if form.validate_on_submit():
        new_machine = Machine(
            name=form.name.data,
            total_available=form.total_available.data
        )
        db.session.add(new_machine)
        db.session.commit()
        flash('Machine added successfully!', 'success')
        return redirect(url_for('admin.manage_machines'))
    
    machines = Machine.query.all()
    return render_template('admin/manage_machines.html', form=form, machines=machines)


@admin_bp.route('/machine/edit/<int:id>', methods=['GET', 'POST'])
def edit_machine(id):
    verify_login()
    machine = Machine.query.get(id)
    form = MachineForm(obj=machine)
    
    if form.validate_on_submit():
        machine.name = form.name.data
        machine.total_available = form.total_available.data
        db.session.commit()
        flash('Machine updated successfully!', 'success')
        return redirect(url_for('admin.manage_machines'))
    
    return render_template('admin/edit_machine.html', form=form, machine=machine)


@admin_bp.route('/machine/delete/<int:id>', methods=['GET'])
def delete_machine(id):
    verify_login()
    machine = Machine.query.get(id)
    if machine:
        db.session.delete(machine)
        db.session.commit()
        flash('Machine deleted successfully!', 'success')
    return redirect(url_for('admin.manage_machines'))
@admin_bp.route('/machine/add', methods=['GET', 'POST'])
def add_machine():
    verify_login()
    form = MachineForm()
    
    if form.validate_on_submit():
        new_machine = Machine(
            name=form.name.data,
            type=form.type.data,  # Assuming you have a type field in the form
            total_available=form.total_available.data
        )
        db.session.add(new_machine)
        db.session.commit()
        flash('Machine added successfully!', 'success')
        return redirect(url_for('admin.manage_machines'))
    
    return render_template('admin/add_machine.html', form=form)


# Manpower Management
@admin_bp.route('/manpower', methods=['GET', 'POST'])
def manage_manpower():
    verify_login()
    form = ManpowerForm()
    if form.validate_on_submit():
        new_person = Manpower(
            role=form.role.data,
            total_available=form.total_available.data
        )
        db.session.add(new_person)
        db.session.commit()
        flash('Manpower added successfully!', 'success')
        return redirect(url_for('admin.manage_manpower'))
    
    manpower = Manpower.query.all()
    return render_template('admin/manage_manpower.html', form=form, manpower=manpower)


@admin_bp.route('/manpower/edit/<int:id>', methods=['GET', 'POST'])
def edit_manpower(id):
    verify_login()
    person = Manpower.query.get(id)
    form = ManpowerForm(obj=person)
    
    if form.validate_on_submit():
        person.role = form.role.data
        person.total_available = form.total_available.data
        db.session.commit()
        flash('Manpower updated successfully!', 'success')
        return redirect(url_for('admin.manage_manpower'))
    
    return render_template('admin/edit_manpower.html', form=form, manpower=person)

@admin_bp.route('/manpower/add', methods=['GET', 'POST'])
def add_manpower():
    verify_login()
    manpower = Manpower.query.get(id)
    form = Manpower(obj=manpower)
    
    if form.validate_on_submit():
        manpower.role = form.role.data
        manpower.total_available = form.total_available.data
        db.session.commit()
        flash('manpower updated successfully!', 'success')
        return redirect(url_for('admin.manage_manpower'))
    
    return render_template('admin/edit_manpower.html', form=form, manpower=manpower)


@admin_bp.route('/manpower/delete/<int:id>', methods=['GET'])
def delete_manpower(id):
    verify_login()
    person = Manpower.query.get(id)
    if person:
        db.session.delete(person)
        db.session.commit()
        flash('Manpower deleted successfully!', 'success')
    return redirect(url_for('admin.manage_manpower'))

# Material Management
@admin_bp.route('/materials', methods=['GET', 'POST'])
def manage_materials():
    verify_login()
    form = MaterialForm()
    if form.validate_on_submit():
        new_material = Material(
            name=form.name.data,
            total_available=form.total_available.data
        )
        db.session.add(new_material)
        db.session.commit()
        flash('Material added successfully!', 'success')
        return redirect(url_for('admin.manage_materials'))
    
    materials = Material.query.all()
    return render_template('admin/manage_materials.html', form=form, materials=materials)


@admin_bp.route('/material/edit/<int:id>', methods=['GET', 'POST'])
def edit_material(id):
    verify_login()
    material = Material.query.get(id)
    form = MaterialForm(obj=material)
    
    if form.validate_on_submit():
        material.name = form.name.data
        material.total_available = form.total_available.data
        db.session.commit()
        flash('Material updated successfully!', 'success')
        return redirect(url_for('admin.manage_materials'))
    
    return render_template('admin/edit_material.html', form=form, material=material)

@admin_bp.route('/material/add', methods=['GET', 'POST'])
def add_material():
    verify_login()
    material = Material.query.get(id)
    form = MaterialForm(obj=material)
    
    if form.validate_on_submit():
        material.name = form.name.data
        material.total_available = form.total_available.data
        db.session.commit()
        flash('material updated successfully!', 'success')
        return redirect(url_for('admin.manage_materials'))
    
    return render_template('admin/edit_material.html', form=form, material=material)


@admin_bp.route('/material/delete/<int:id>', methods=['GET'])
def delete_material(id):
    verify_login()
    material = Material.query.get(id)
    if material:
        db.session.delete(material)
        db.session.commit()
        flash('Material deleted successfully!', 'success')
    return redirect(url_for('admin.manage_materials'))

# --- Repair Management Routes ---

@admin_bp.route('/repairs', methods=['GET'])
def manage_repairs():
    verify_login()
    repairs = Repair.query.all()
    return render_template('admin/manage_repairs.html', repairs=repairs)


# --- Admin Dashboard ---
@admin_bp.route('/')
def home_page():
    verify_login()
    complaints = Complaint.query.all()
    repairs = Repair.query.all()
    machines = Machine.query.all()
    manpower = Manpower.query.all()
    materials = Material.query.all()
    repair_details = []
    for repair in repairs:
        complaint = Complaint.query.get(repair.complaint_id)
        details = {
            'id': repair.id,
            'location': complaint.location,
            'status': repair.status,
            'description': complaint.description,
            'start_date': repair.start_date,
            'completion_date': repair.completion_date if repair.completion_date else "Not Completed",
        }
        repair_details.append(details)

    return render_template('admin/dashboard.html', complaints=complaints, repairs=repairs, machines=machines, manpower=manpower, materials=materials, repair_details=repair_details)

