from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, Length
from .models import User, Complaint, Repair, Resource 

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

# Register Form (if not already included)
class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_no = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    role = SelectField('Role', choices=[('resident', 'Resident'), ('supervisor', 'Supervisor'), ('admin', 'Administrator')])
    submit = SubmitField('Register')

# User Form
class UserForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_no = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('supervisor', 'Supervisor'), ('resident', 'Resident')])
    submit = SubmitField('Register')

# Complaint Form
class ComplaintForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    severity = SelectField('Severity', choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High'), ('4', 'Critical')])
    submit = SubmitField('Submit Complaint')

# Repair Form
class RepairForm(FlaskForm):
    complaint_id = IntegerField('Complaint ID', validators=[DataRequired()])
    supervisor_id = IntegerField('Supervisor ID')
    start_date = DateTimeField('Start Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    expected_completion_date = DateTimeField('Expected Completion Date', format='%Y-%m-%d %H:%M:%S')
    status = SelectField('Status', choices=[('Scheduled', 'Scheduled'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    submit = SubmitField('Update Repair')

# Resource Form
class ResourceForm(FlaskForm):
    name = StringField('Resource Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Material', 'Material'), ('Machinery', 'Machinery'), ('Labor', 'Labor')])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    allocated_to = IntegerField('Allocated to Repair ID', default=None)
    submit = SubmitField('Add Resource')
