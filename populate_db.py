from datetime import datetime
from backend.app.models import db, User, BranchOffice, ResourceMaterial, ResourceManpower, ResourceMachine
from app import app  # Assuming your Flask app is initialized in app.py

def populate_db():
    with app.app_context():
        # Add Users (Residents, Supervisors, Clerks, Admin, Mayor)
        users = [
            # Residents
            User(name="Resident 1", username="resident1", email="resident1@gmail.com", phone_no="0000000000", password="12345678", role="resident"),
            User(name="Resident 2", username="resident2", email="resident2@gmail.com", phone_no="0000000001", password="12345678", role="resident"),
            User(name="Resident 3", username="resident3", email="resident3@gmail.com", phone_no="0000000002", password="12345678", role="resident"),
            User(name="Resident 4", username="resident4", email="resident4@gmail.com", phone_no="0000000003", password="12345678", role="resident"),
            User(name="Resident 5", username="resident5", email="resident5@gmail.com", phone_no="0000000004", password="12345678", role="resident"),

            # Supervisors
            User(name="Supervisor 1", username="supervisor1", email="supervisor1@gmail.com", phone_no="1110000000", password="12345678", role="supervisor"),
            User(name="Supervisor 2", username="supervisor2", email="supervisor2@gmail.com", phone_no="1110000001", password="12345678", role="supervisor"),
            User(name="Supervisor 3", username="supervisor3", email="supervisor3@gmail.com", phone_no="1110000002", password="12345678", role="supervisor"),
            User(name="Supervisor 4", username="supervisor4", email="supervisor4@gmail.com", phone_no="1110000003", password="12345678", role="supervisor"),
            User(name="Supervisor 5", username="supervisor5", email="supervisor5@gmail.com", phone_no="1110000004", password="12345678", role="supervisor"),

            # Clerks
            User(name="Clerk 1", username="clerk1", email="clerk1@gmail.com", phone_no="2220000000", password="12345678", role="clerk"),
            User(name="Clerk 2", username="clerk2", email="clerk2@gmail.com", phone_no="2220000001", password="12345678", role="clerk"),
            User(name="Clerk 3", username="clerk3", email="clerk3@gmail.com", phone_no="2220000002", password="12345678", role="clerk"),
            User(name="Clerk 4", username="clerk4", email="clerk4@gmail.com", phone_no="2220000003", password="12345678", role="clerk"),
            User(name="Clerk 5", username="clerk5", email="clerk5@gmail.com", phone_no="2220000004", password="12345678", role="clerk"),

            # Admins
            User(name="Admin 1", username="admin1", email="admin1@gmail.com", phone_no="3330000000", password="12345678", role="admin"),
            User(name="Admin 2", username="admin2", email="admin2@gmail.com", phone_no="3330000001", password="12345678", role="admin"),
            User(name="Admin 3", username="admin3", email="admin3@gmail.com", phone_no="3330000002", password="12345678", role="admin"),
            User(name="Admin 4", username="admin4", email="admin4@gmail.com", phone_no="3330000003", password="12345678", role="admin"),
            User(name="Admin 5", username="admin5", email="admin5@gmail.com", phone_no="3330000004", password="12345678", role="admin"),

            # Mayor
            User(name="Mayor", username="mayor", email="mayor@gmail.com", phone_no="4440000000", password="12345678", role="mayor")
        ]

        db.session.add_all(users)
        db.session.commit()

        # Add Branches with supervisors assigned
        branches = [
            BranchOffice(name="Branch 1", supervisor_id=6, location="Location 1"),
            BranchOffice(name="Branch 2", supervisor_id=7, location="Location 2"),
            BranchOffice(name="Branch 3", supervisor_id=8, location="Location 3"),
            BranchOffice(name="Branch 4", supervisor_id=9, location="Location 4"),
            BranchOffice(name="Branch 5", supervisor_id=10, location="Location 5")
        ]

        db.session.add_all(branches)
        db.session.commit()

        # Add Resource Materials
        materials = [
            ResourceMaterial(name="Asphalt", total_available=12000.0, currently_allocated=0, currently_requested=0, in_use=0, unit="kg", status="Available"),
            ResourceMaterial(name="Bitumen", total_available=8000.0, currently_allocated=0, currently_requested=0, in_use=0, unit="kg", status="Available"),
            ResourceMaterial(name="Concrete", total_available=5000.0, currently_allocated=0, currently_requested=0, in_use=0, unit="kg", status="Available"),
            ResourceMaterial(name="Gravel", total_available=15000.0, currently_allocated=0, currently_requested=0, in_use=0, unit="kg", status="Available"),
            ResourceMaterial(name="Sand", total_available=20000.0, currently_allocated=0, currently_requested=0, in_use=0, unit="kg", status="Available")
        ]

        db.session.add_all(materials)
        db.session.commit()

        # Add Resource Manpower
        manpower = [
            ResourceManpower(role="Laborer", total_available=100, in_use=0, currently_allocated=0, currently_requested=0, status="Available"),
            ResourceManpower(role="Supervisor", total_available=10, in_use=0, currently_allocated=0, currently_requested=0, status="Available"),
            ResourceManpower(role="Engineer", total_available=5, in_use=0, currently_allocated=0, currently_requested=0, status="Available")
        ]

        db.session.add_all(manpower)
        db.session.commit()

        # Add Resource Machines
        machines = [
            ResourceMachine(name="Excavator", total_available=5, currently_allocated=0, in_use=0, currently_requested=0, status="Available"),
            ResourceMachine(name="Bulldozer", total_available=3, currently_allocated=0, in_use=0, currently_requested=0, status="Available"),
            ResourceMachine(name="Cement Mixer", total_available=4, currently_allocated=0, in_use=0, currently_requested=0, status="Available")
        ]

        db.session.add_all(machines)
        db.session.commit()

        print("Database populated with dummy values!")

if __name__ == "__main__":
    populate_db()
