from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_no: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    complaints = db.relationship('Complaint', backref='user', lazy=True)

    def __init__(self, name, username, email, phone_no, password, role):
        self.name = name
        self.username = username
        self.email = email
        self.phone_no = phone_no
        self.password = password
        self.role = role

    def __repr__(self):
        return f'<User {self.username}>'

class Complaint(db.Model):
    __tablename__ = 'complaint'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user.id'), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    repair = db.relationship('Repair', backref='complaint', lazy=True)

    def __init__(self, user_id, location, description, severity="Pending", status="Pending", repair=None):
        self.user_id = user_id
        self.location = location
        self.description = description
        self.severity = severity
        self.status = status
        self.repair = repair

    def __repr__(self):
        return f'<Complaint {self.id}>'

class Resource(db.Model):
    __tablename__ = 'resource'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    allocated_to: Mapped[int] = mapped_column(Integer, db.ForeignKey('repair.id'), nullable=True)

    def __init__(self, name, category, quantity, unit, allocated_to=None):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.unit = unit
        self.allocated_to = allocated_to

    def __repr__(self):
        return f'<Resource {self.name}>'

class Repair(db.Model):
    __tablename__ = 'repair'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    complaint_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('complaint.id'), nullable=False)
    supervisor_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default="Scheduled")
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    completion_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    expected_completion_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # Define relationships without using mapped_column
    resources_allocated = db.relationship('Resource', backref='repair', lazy=True)

    def __init__(self, complaint_id, supervisor_id=None, status="Scheduled", start_date=None, expected_completion_date=None):
        self.complaint_id = complaint_id
        self.supervisor_id = supervisor_id
        self.status = status
        self.start_date = start_date
        self.completion_date = None
        self.expected_completion_date = expected_completion_date

    def __repr__(self):
        return f'<Repair {self.id}>'

# Initialize DB (call this in main.py)
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()