from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_no = db.Column(db.String(10), unique=True, nullable=False)  # Fixed issue
    password = db.Column(db.String(100), nullable=False)  # Removed min=8 (validate in app)
    role = db.Column(db.String(20), nullable=False)  # "admin", "supervisor", "resident"
    complaints = db.relationship('Complaint', backref='user', lazy=True)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False, server_default="No description provided")  # Fixed issue
    severity = db.Column(db.String(50), nullable=False, server_default="Not Rated yet")  # Fixed issue
    status = db.Column(db.String(50), nullable=False, server_default="Pending")  # Added server_default
    repair = db.relationship('Repair', backref='complaint', lazy=True)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Resource Name (e.g., Cement, Excavator)
    category = db.Column(db.String(50), nullable=False)  # Material, Machinery, Labor, etc.
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit = db.Column(db.String(50), nullable=False)  # Ton, Liters, Pieces, etc.
    required = db.Column(db.Boolean, default=True)  # Is required status
    allocated_to = db.Column(db.Integer, db.ForeignKey('repair.id'), nullable=True)  # Assigned repair task

class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    status = db.Column(db.String(50), nullable=False, server_default="Scheduled")  # Fixed issue
    resources_used = db.relationship('Resource', backref='repair', lazy=True)
    expected_completion_date = db.Column(db.DateTime, nullable=False)  # Fixed typo

# Initialize DB (call this in main.py)
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()