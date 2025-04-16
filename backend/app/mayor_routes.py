from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from .models import db, BranchOffice,User, Complaint, Repair, RepairMachineAllocation, RepairManpowerAllocation, RepairMaterialAllocation
from .models import ResourceMachine, ResourceManpower, ResourceMaterial, RepairSchedule
import datetime 
mayor_bp = Blueprint('mayor', __name__)

@mayor_bp.route("/")
def home_page():
    if 'mayor' not in session.get("user_type", ""):
        return redirect(url_for('main.home'))

    all_repairs = db.session.query(Repair).filter().all()
    # print('\n\n\n\n\n\n\n\n\n',all_repairs)
    repair_details = []
    for repair in all_repairs:
        # print('\n', repair.id)
        complaint = Complaint.query.get(repair.complaint_id)
        details = {
            'id': repair.id,
            'location': complaint.location,
            'status': repair.status,
            'description': complaint.description,
            'start_date': repair.start_date.strftime("%Y-%m-%d") if repair.start_date else "Not Started",
            'completion_date': repair.completion_date.strftime("%Y-%m-%d") if repair.completion_date else "Not Completed",
        }
        repair_details.append(details)
    # print(repair_details)
    complaints = Complaint.query.all()
    users = User.query.all()

    chart_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'june', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    chart_days = [i for i in range(1,32)]
    current_year = int(datetime.datetime.today().strftime('%y'))
    chart_years = [i for i in range(current_year-5, current_year+5)]

    monthly_repairs = [0]*12
    yearly_repairs = [0]*10
    dayly_repairs = [0]*31
    for repair in repair_details:
        if repair['status'] == 'Completed':
            if repair['start_date'] != 'Not Started':
                year, month, day = str(repair['completion_date']).split('-')
                monthly_repairs[int(month)-1]+=1
                yearly_repairs[int(year)%current_year-5]+=1
                dayly_repairs[int(day)-1]+=1
                
    

    return render_template(
        "mayor/dashboard.html",
        repairs=all_repairs,
        complaints=complaints,
        users=users,
        repair_details=repair_details,
        chart_years = chart_years,
        chart_months=chart_months,
        chart_days = chart_days,
        yearly_repairs =yearly_repairs,
        monthly_repairs=monthly_repairs,
        dayly_repairs = dayly_repairs,
        total_complaints = len(complaints),
        completed_repairs=len(db.session.query(Repair).filter(Repair.status=="Completed").all()),
        ongoing_repairs = len(db.session.query(Repair).filter(Repair.status=="In Progress").all()),
        scheduled_repairs = len(db.session.query(Repair).filter(Repair.status=="Scheduled").all()),
    )