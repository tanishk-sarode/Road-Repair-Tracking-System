from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import ComplaintForm, RepairForm, ResourceManpowerForm, ResourceMachineForm, LoginForm, RegisterForm
from .models import db, Complaint, Repair, User, ResourceManpower, ResourceMachine


auth_bp = Blueprint('auth', __name__)

# Register User
@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    login_form = LoginForm()

    if register_form.validate_on_submit():
        hashed_password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256')

        new_user = User(
            name=register_form.name.data,
            username=register_form.username.data,
            email=register_form.email.data,
            phone_no=register_form.phone_no.data,
            password=hashed_password,
            role=register_form.role.data
        )

        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template('login.html', login_form=login_form, register_form=register_form)


# Login User
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter((User.username == username) | (User.email == username)).first()
        
        if user and check_password_hash(user.password, password) or user.password==password:  # Use hashed password check
            session["user_id"] = user.id  
            session["user_type"] = user.role
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))
        
        flash("Invalid username or password", "danger")

    return render_template('login.html', login_form=login_form, register_form=register_form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))  


@auth_bp.route("/resident/dashboard")
def resident_dashboard():
    if "user_id" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])
    complaints = Complaint.query.filter_by(residence_id=session["user_id"]).all()
    repairs = Repair.query.filter(Repair.complaint_id.in_([c.id for c in complaints])).all()

    form = ComplaintForm()

    return render_template(
        "resident_dashboard.html",
        user=user,
        complaints=complaints,
        repairs=repairs,
        form=form  
    )