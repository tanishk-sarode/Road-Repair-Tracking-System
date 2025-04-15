from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Complaint, Repair, User, ResourceManpower, ResourceMachine
from .forms import ComplaintForm, RepairForm, ResourceManpowerForm, ResourceMachineForm, LoginForm, RegisterForm

from .auth import auth_bp

resident_bp = Blueprint('resident', __name__)

@resident_bp.route('/home_page')
def home_page():
    user_type = session.get("user_type")
    user_id = session.get("user_id")
    if user_type != "resident":
        flash("Access denied. Please log in to continue.", "danger")
    #     return redirect(url_for("auth.login"))
    # user_complaints = db.session.query(Complaint).filter_by(residence_id=session["user_id"]).all()
    user_complaints = db.session.execute(db.select(Complaint)).scalars().all()
    Complaints = []
    for complaint in user_complaints:
        Complaints.append({
            "id": f"C{user_id}{complaint.id}",
            "description": complaint.description,
            "status": complaint.status,
            "date": complaint.date_reported.strftime("%Y-%m-%d"),
        })
    return render_template('resident.html', complaints=Complaints)

