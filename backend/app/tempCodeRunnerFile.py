from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from datetime import datetime, timezone

db = SQLAlchemy()

class BranchOffice(db.Model):
    __tablename__ = 'branch_office'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    supervisor_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    complaints = db.relationship('Complaint', backref='branch_office', lazy=True)

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_no: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)

    # Relationships
    complaints_clerk = db.relationship('Complaint', foreign_keys='Complaint.clerk_id', backref='clerk', lazy=True)
    complaints_resident = db.relationship('Complaint', foreign_keys='Complaint.residence_id', backref='resident', lazy=True)
    repairs = db.relationship('Repair', backref='supervisor', lazy=True)
    branches = db.relationship('BranchOffice', foreign_keys='BranchOffice.supervisor_id', backref='supervisor', lazy=True)

class Complaint(db.Model):
    __tablename__ = 'complaint'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clerk_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    residence_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    branch_office_id: Mapped[int] = mapped_column(Integer, ForeignKey('branch_office.id'), nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    date_reported: Mapped[DateTime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    repair = db.relationship('Repair', backref='complaint', lazy=True, uselist=False)

class Repair(db.Model):
    __tablename__ = 'repair'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    complaint_id: Mapped[int] = mapped_column(Integer, ForeignKey('complaint.id'), nullable=False)
    supervisor_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Scheduled")
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    completion_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    expected_completion_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    manpower_allocations = db.relationship('ResourceManpower', backref='repair', lazy=True)
    machine_allocations = db.relationship('ResourceMachine', backref='repair', lazy=True)

class ResourceManpower(db.Model):
    __tablename__ = 'resource_manpower'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    total_available: Mapped[int] = mapped_column(Integer, nullable=False)
    currently_allocated: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    repair_id: Mapped[int] = mapped_column(Integer, ForeignKey('repair.id'), nullable=True)

class ResourceMachine(db.Model):
    __tablename__ = 'resource_machine'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    total_available: Mapped[int] = mapped_column(Integer, nullable=False)
    currently_allocated: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Available")
    repair_id: Mapped[int] = mapped_column(Integer, ForeignKey('repair.id'), nullable=True)

class RepairSchedule(db.Model):
    __tablename__ = 'repair_schedule'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    repair_id: Mapped[int] = mapped_column(Integer, ForeignKey('repair.id'), nullable=False)
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Planned")

class AdminAction(db.Model):
    __tablename__ = 'admin_action'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    change_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

# Initialize DB
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
