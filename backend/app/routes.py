from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .models import db, Complaint, Repair, Resource

main_bp = Blueprint('main', __name__)

# Get all complaints
@main_bp.route('/complaints', methods=['GET'])
def get_complaints():
    complaints = Complaint.query.all()
    return jsonify([{
        "id": c.id,
        "location": c.location,
        "description": c.description,
        "severity": c.severity,
        "status": c.status
    } for c in complaints])

# Submit a new complaint
@main_bp.route('/complaints', methods=['POST'])
def submit_complaint():
    data = request.json
    complaint = Complaint(
        user_id=data['user_id'],
        location=data['location'],
        description=data['description'],
        severity=data['severity']
    )
    db.session.add(complaint)
    db.session.commit()
    return jsonify({"message": "Complaint submitted successfully"}), 201

# Get all repairs
@main_bp.route('/repairs', methods=['GET'])
def get_repairs():
    repairs = Repair.query.all()
    return jsonify([{
        "id": r.id,
        "complaint_id": r.complaint_id,
        "status": r.status
    } for r in repairs])



@main_bp.route('/')
def home():
    return render_template('index.html')  # Renders homepage

@main_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Dummy authentication logic
    if username == "admin" and password == "admin123":
        return redirect(url_for("main.adminstrator"))
    
    return render_template("index.html", error_message="Invalid username or password")

@main_bp.route("/register", methods=["POST"])
def register():
    new_username = request.form.get("newUsername")
    role = request.form.get("role")
    new_password = request.form.get("newPassword")
    
    # Dummy registration logic
    return render_template("index.html", register_message="Registration successful! Now login.")





@main_bp.route("/dashboard")
def dashboard():
    return render_template("adminstrator.html")  

@main_bp.route("/complaints")  
def complaints():
    return render_template("complaints.html")

@main_bp.route("/repairs")  
def repairs():
    return render_template("repairs.html")

@main_bp.route("/reports")  # only admin and mayor can access this route
def reports():
    return render_template("reports.html")

@main_bp.route("/resources")  # only admin can access this route
def resources():
    return render_template("resources.html")

