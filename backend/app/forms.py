from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, DateField, FormField, IntegerField, TextAreaField, SelectField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

# Register Form
class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_no = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)], default='0000000000')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    role = SelectField('Role', choices=[('resident', 'Resident'), ('supervisor', 'Supervisor'), ('admin', 'Administrator')])
    status = HiddenField(default='New')
    submit = SubmitField('Register')

# Complaint Form

class ComplaintForm(FlaskForm):
    residence_id = SelectField("Residence", coerce=int, validators=[DataRequired()])
    branch_office_id = SelectField("Branch Office", coerce=int, validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    severity = SelectField("Severity", choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")], validators=[DataRequired()])
    submit = SubmitField("Submit")

class RepairForm(FlaskForm):
    machine_ids = FieldList(IntegerField('Machine ID'), min_entries=0)
    machine_quantities = FieldList(IntegerField('Quantity'), min_entries=0)

    manpower_ids = FieldList(IntegerField('Manpower ID'), min_entries=0)
    manpower_quantities = FieldList(IntegerField('Quantity'), min_entries=0)

    material_ids = FieldList(IntegerField('Material ID'), min_entries=0)  # 🆕
    material_quantities = FieldList(IntegerField('Quantity'), min_entries=0)  # 🆕

    priority = SelectField(
        'Priority',
        coerce=int,
        choices=[(1, 'Lowest'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Extreme')],
        validators=[DataRequired()]
    )
    complaint_id = HiddenField('Complaint ID')
    days_to_complete = IntegerField('Days to Complete', default=1, validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Assign Repair')



    def populate_choices(self, machines, manpower, material):
        # Set main dropdowns
        self.machines.choices = [(m.id, m.name) for m in machines]
        self.manpower.choices = [(mp.id, mp.role) for mp in manpower]
        self.material.choices = [(m.id, m.name) for m in material]

        # Set nested form dropdowns (for dynamic machine and manpower allocations)
        machine_choices = [(m.id, m.name) for m in machines]
        manpower_choices = [(mp.id, mp.role) for mp in manpower]
        material_choices = [(m.id, m.name) for m in material]
        for subform in self.material_allocations:
            subform.material_id.choices = material_choices
        for subform in self.machine_allocations:
            subform.machine_id.choices = machine_choices

        for subform in self.manpower_allocations:
            subform.manpower_id.choices = manpower_choices

# Resource Manpower Form
class ResourceManpowerForm(FlaskForm):
    role = StringField('Role', validators=[DataRequired()])
    total_available = IntegerField('Total Available', validators=[DataRequired()])
    currently_allocated = IntegerField('Currently Allocated', default=0)
    repair_id = IntegerField('Allocated to Repair ID', default=None)
    submit = SubmitField('Add Manpower')

# Resource Machine Form
class ResourceMachineForm(FlaskForm):
    name = StringField('Machine Name', validators=[DataRequired()])
    total_available = IntegerField('Total Available', validators=[DataRequired()])
    currently_allocated = IntegerField('Currently Allocated', default=0)
    status = SelectField('Status', choices=[('Available', 'Available'), ('In Use', 'In Use'), ('Under Maintenance', 'Under Maintenance')])
    repair_id = IntegerField('Allocated to Repair ID', default=None)
    submit = SubmitField('Add Machine')

class ResourceMaterialForm(FlaskForm):
    name = StringField('Material Name', validators=[DataRequired()])
    unit = StringField('Unit (e.g., kg, liters)', validators=[DataRequired()])
    total_available = IntegerField('Total Available', validators=[DataRequired()])
    currently_allocated = IntegerField('Currently Allocated', default=0)
    status = SelectField('Status', choices=[('Available', 'Available'), ('In Use', 'In Use')], default='Available')
    submit = SubmitField('Add Material')


# Repair Schedule Form
class RepairScheduleForm(FlaskForm):
    repair_id = IntegerField('Repair ID', validators=[DataRequired()])
    start_date = DateTimeField('Start Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    end_date = DateTimeField('End Date', format='%Y-%m-%d %H:%M:%S')
    status = SelectField('Status', choices=[('Planned', 'Planned'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')])
    submit = SubmitField('Schedule Repair')

# Admin Action Form
class AdminActionForm(FlaskForm):
    resource_type = SelectField('Resource Type', choices=[('Material', 'Material'), ('Machinery', 'Machinery'), ('Labor', 'Labor')], validators=[DataRequired()])
    resource_id = IntegerField('Resource ID', validators=[DataRequired()])
    action_type = SelectField('Action Type', choices=[('Add', 'Add'), ('Remove', 'Remove'), ('Update', 'Update')], validators=[DataRequired()])
    change_quantity = IntegerField('Change Quantity', validators=[DataRequired()])
    submit = SubmitField('Record Action')

# Branch Office Form
class BranchOfficeForm(FlaskForm):
    name = StringField('Branch Office Name', validators=[DataRequired(), Length(max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Add Branch Office')

class UpdateRepairCalenderDate(FlaskForm):
    repair_id = HiddenField('Repair ID', validators=[DataRequired()])
    start_date = DateField('New Start Date', validators=[DataRequired()])
    expected_completion_date = DateField('New End Date', validators=[DataRequired()])
    submit = SubmitField('Update')

class UpdateResourceForm(FlaskForm):
    resource_id = HiddenField('Resource ID', validators=[DataRequired()])
    resource_type = SelectField('Resource Type', choices=[('Material', 'Material'), ('Machinery', 'Machinery'), ('Labor', 'Labor')], validators=[DataRequired()])
    resource_name = StringField('Resource Name', validators=[DataRequired(), Length(max=100)])
    total_available = IntegerField('Total Available', validators=[DataRequired()])
    currently_allocated = IntegerField('Currently Allocated', default=0)
    submit = SubmitField('Update Resource')