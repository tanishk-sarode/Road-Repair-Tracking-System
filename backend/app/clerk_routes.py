from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from .models import db, Complaint,BranchOffice, Repair, User, ResourceManpower, ResourceMachine
from .forms import ComplaintForm, RepairForm, ResourceManpowerForm, ResourceMachineForm, LoginForm, RegisterForm
from .auth import auth_bp

clerk_bp = Blueprint('clerk', __name__)


@clerk_bp.route("/home_page", methods=['GET'])
def home_page():
    if "user_id" not in session:
        flash("You need to log in first!", "warning")
        return redirect(url_for("main.login"))
    
    username = db.session.query(User).filter_by(id=session["user_id"]).first().name
    
    all_complaints = db.session.execute(db.select(Complaint).where(Complaint.status!='Completed')).scalars().all()
    complaints_list = []
    for complaints in all_complaints:
        complaints_list.append({
            "id": complaints.id,
            "description": complaints.description,
            "location": complaints.location,
            "severity": complaints.severity,
            "status": complaints.status,
            "date": complaints.date_reported.strftime("%Y-%m-%d %H:%M") if complaints.date_reported else "N/A",
            "clerk_id": complaints.clerk_id,
            "residence_id": complaints.residence_id,
            "branch_office_id": complaints.branch_office_id,
            "branch": db.session.query(BranchOffice).filter_by(id=complaints.branch_office_id).first().name

        })

    # complaints_list =  jsonify(complaints=complaints_list)
    return render_template("clerk/clerk.html", complaints=complaints_list,user=username)
    




@clerk_bp.route("/add_complaints", methods=["GET", "POST"])
def add_complaints():
    if request.method == "POST":
        print("FORM DATA:", request.form)  # 👈 add this

    form = ComplaintForm()

    # Populate choices for residence_id and branch_office_id
    residences = db.session.query(User).filter_by(role='resident').all()
    offices = BranchOffice.query.all()

    form.residence_id.choices = [(res.id, res.name) for res in residences]
    form.branch_office_id.choices = [(office.id, office.name) for office in offices]

    if form.validate_on_submit():
        new_complaint = Complaint(
            clerk_id=session["user_id"],
            residence_id=form.residence_id.data,
            branch_office_id=form.branch_office_id.data,
            location=form.location.data,
            description=form.description.data,
            severity=form.severity.data,
            status="Unaccepted",  # Default status
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash("Complaint submitted successfully!", "success")
        return redirect(url_for("clerk.home_page"))
    else:
        print(form.errors)  # Log validation errors for debugging

    return render_template("clerk/add_complaints.html", form=form)

@clerk_bp.route("/edit_complaint/<int:id>", methods=["GET", "POST"])
def edit_complaint(id):
    if "user_id" not in session:
        flash("You need to log in first!", "warning")
        return redirect(url_for("main.login"))
    
    complaint = db.session.query(Complaint).filter_by(id=id).first()

    if not complaint:
        flash("Complaint not found", "danger")
        return redirect(url_for("clerk.home_page"))
    
    form = ComplaintForm(obj=complaint)

    # Populate choices for residence_id and branch_office_id
    residences = db.session.query(User).filter_by(role='resident').all()
    offices = BranchOffice.query.all()

    form.residence_id.choices = [(res.id, res.name) for res in residences]
    form.branch_office_id.choices = [(office.id, office.name) for office in offices]

    if form.validate_on_submit():
        action = request.form.get('action')
        if action == "delete":
            db.session.delete(complaint)
            db.session.commit()
            flash("Complaint deleted successfully!", "success")
            return redirect(url_for("clerk.home_page"))
        if action == "cancel":
            return redirect(url_for("clerk.home_page"))
        complaint.residence_id = form.residence_id.data
        complaint.branch_office_id = form.branch_office_id.data
        complaint.location = form.location.data
        complaint.description = form.description.data
        complaint.severity = form.severity.data

        db.session.commit()
        flash("Complaint updated successfully!", "success")
        return redirect(url_for("clerk.home_page"))

    return render_template("clerk/edit_complaint.html", form=form, complaint=complaint)
