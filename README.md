# Road Repair Tracking System (RRTS)

The **Road Repair Tracking System** is a web-based application designed to streamline the process of managing road repair complaints, resource allocation, and repair scheduling. It provides role-based dashboards for residents, clerks, supervisors, administrators, and mayors to efficiently handle their respective tasks.

---

## Features

### For Residents:
- Submit complaints about road issues.
- View the status of submitted complaints.

### For Clerks:
- Manage complaints submitted by residents.
- Edit, delete, or update complaints.

### For Supervisors:
- View and accept complaints assigned to their branch.
- Allocate resources (machines and manpower) for repairs.
- Schedule repairs and update repair timelines.
- View all ongoing and completed repairs.

### For Administrators:
- Manage available resources (machines and manpower).
- Monitor resource usage and allocation.

### For Mayors:
- View monthly reports on complaints, repairs, and resource usage.

---

## Project Structure

```
Road-Repair-Tracking-System/
│
├── backend/                     # Flask Backend
│   ├── app/
│   │   ├── __init__.py          # Initializes Flask app
│   │   ├── models.py            # Database models
│   │   ├── routes.py            # API endpoints
│   │   ├── auth.py              # Authentication logic
│   │   ├── config.py            # App configurations
│   │   ├── supervisor_routes.py # Supervisor-specific routes
│   │   ├── clerk_routes.py      # Clerk-specific routes
│   │   ├── resident_routes.py   # Resident-specific routes
│   ├── requirements.txt         # Backend dependencies
│
├── frontend/                    # Frontend (HTML, CSS, JS)
│   ├── static/                  # CSS, JS, images
│   ├── templates/               # HTML templates (Jinja2)
│   ├── index.html               # Main page
│
├── database/                    # Database & Migrations
│   ├── schema.sql               # SQL schema
│   ├── seed.py                  # Initial database seeding script
│
├── .env                         # Environment variables
├── .gitignore                   # Ignore unnecessary files
├── README.md                    # Project documentation
```

---

## Technologies Used

### Backend:
- **Flask**: Python web framework.
- **Flask-SQLAlchemy**: ORM for database management.
- **Flask-WTF**: Form handling and validation.
- **SQLite**: Lightweight database for development.

### Frontend:
- **HTML/CSS**: For structure and styling.
- **Bootstrap**: Responsive design and UI components.
- **JavaScript**: Dynamic interactions and functionality.

---

## Installation and Setup

### Prerequisites:
- Python 3.8 or higher
- pip (Python package manager)

### Steps:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/tanishk-sarode/Road-Repair-Tracking-System.git
   cd Road-Repair-Tracking-System
   ```

2. **Set up the backend:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   - Configure the database in `backend/app/config.py`.
   - Initialize the database:
     ```bash
     python -m backend.app.models
     ```
   - Populate Database with Dummy Values
      ```bash
      python populate_db.py
      ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## Usage

### Roles and Responsibilities:
- **Resident**: Submit and track complaints.
- **Clerk**: Manage complaints and assign them to supervisors.
- **Supervisor**: Allocate resources and schedule repairs.
- **Administrator**: Manage resources.
- **Mayor**: View reports and monitor progress.

---

## Screenshots

### Mayor Dashboard:
![Mayor Dashboard](/documents/screensorts/Mayor_dashboard.png)

### Supervisor Dashboard:
![Supervisor Dashboard](/documents/screensorts/supervisor_dashboard.png)
![Supervisor Calender](/documents/screensorts/supervisor_calender.png)

### Admin Dashboard:
![Admin Dashboard](/documents/screensorts/Admin_dashboard.png)

### Clerk Dashboard:
![Clerk Dashboard](/documents/screensorts/clerk_dashboard.png)

### Resident Dashboard:
![Resident Dashboard](/documents/screensorts/Resident_dashboard.png)




---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or feedback, feel free to reach out:
- **Email**: your-email@example.com
- **GitHub**: [your-username](https://github.com/your-username)
