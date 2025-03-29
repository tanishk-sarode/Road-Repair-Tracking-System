from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Complaint, Repair, Resource, User
from .forms import UserForm, ComplaintForm, RepairForm, ResourceForm, LoginForm, RegisterForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    user_type = session.get("user_type")  # Fetch user type from session

    if user_type == "admin":
        return render_template('admin.html')
    elif user_type == "supervisor":
        return render_template('supervisors.html')
    elif user_type == "resident":
        return render_template('residents.html')
    elif user_type == "mayor":
        return render_template('mayor.html')

    # Default to login page if no session exists
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template('login.html', login_form=login_form, register_form=register_form)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter((User.username == username)).first()
        if not user: user = User.query.filter((User.email == username)).first()  # Check by email if username not found
        if user and (user.password == password):  # Check hashed password
            session["user_id"] = user.id  # Store user session
            session["user_type"] = user.role  # Store role for redirection
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))
        
        flash("Invalid username or password", "danger")

    return render_template('login.html', login_form=login_form, register_form=register_form)


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    login_form = LoginForm()
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        new_user = User(
            name=register_form.name.data,
            username=register_form.username.data,
            email=register_form.email.data,
            phone_no=register_form.phone_no.data,
            password=register_form.password,  # Store hashed password
            role=register_form.role.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template('login.html', login_form=login_form, register_form=register_form)


@main_bp.route("/logout")
def logout():
    session.clear()  # Clears all session data
    flash("You have been logged out.", "info")  
    return redirect(url_for("main.home"))  # Redirect to home page


@main_bp.route('/complaints', methods=['GET', 'POST'])
def complaints():
    form = ComplaintForm()
    
    if form.validate_on_submit():
        new_complaint = Complaint(
            user_id=session.get("user_id"),  # Fetch user ID from session
            location=form.location.data,
            description=form.description.data,
            severity=form.severity.data
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash("Complaint submitted successfully!", "success")
        return redirect(url_for("main.complaints"))

    complaints_list = Complaint.query.all()
    return render_template("complaints.html", form=form, complaints=complaints_list)


@main_bp.route('/repairs', methods=['GET', 'POST'])
def repairs():
    form = RepairForm()

    if form.validate_on_submit():
        new_repair = Repair(
            complaint_id=form.complaint_id.data,
            supervisor_id=form.supervisor_id.data,
            start_date=form.start_date.data,
            expected_completion_date=form.expected_completion_date.data,
            status=form.status.data
        )
        db.session.add(new_repair)
        db.session.commit()
        flash("Repair scheduled successfully!", "success")
        return redirect(url_for("main.repairs"))

    repairs_list = Repair.query.all()
    return render_template("repairs.html", form=form, repairs=repairs_list)


@main_bp.route("/reports")
def reports():
    return render_template("reports.html")


@main_bp.route("/resources", methods=["GET", "POST"])
def resources():
    form = ResourceForm()
    
    if form.validate_on_submit():
        new_resource = Resource(
            name=form.name.data,
            category=form.category.data,
            quantity=form.quantity.data,
            unit=form.unit.data
        )
        db.session.add(new_resource)
        db.session.commit()
        flash("Resource added successfully!", "success")
        return redirect(url_for("main.resources"))

    resources_list = Resource.query.all()
    return render_template("resources.html", form=form, resources=resources_list)


# Admin & Role-Based Routes
@main_bp.route("/administrator")
def administrator():
    return render_template("administrator.html")

@main_bp.route("/supervisor")
def supervisor():
    return render_template("supervisors.html")

@main_bp.route("/resident")
def resident():
    return render_template("residents.html")

@main_bp.route("/mayor")
def mayor():
    return render_template("mayor.html")

@main_bp.route("/admin")
def admin():
    return render_template("admin.html")
