# Database Setup Project

This project is designed to set up a Flask application with a database backend. It utilizes SQLAlchemy for ORM (Object-Relational Mapping) to manage database interactions.

## Project Structure

```
Road-Repair-Tracking-System/
│
├── backend/                     # Flask Backend
│   ├── app/
│   │   ├── __init__.py          # Initializes Flask app
│   │   ├── models.py            # database file 
│   │   ├── routes.py            # API endpoints (residents, supervisors, admins)
│   │   ├── auth.py              # Authentication (Flask-Login/JWT)
│   │   ├── config.py            # App configurations
│   │   ├── services.py          # Business logic (handling repairs, scheduling)
│   ├── main.py                  # Entry point for running Flask
│   ├── requirements.txt         # Backend dependencies
│
├── frontend/                    # Frontend (HTML, CSS, JS)
│   ├── static/                  # CSS, JS, images
│   ├── templates/               # HTML templates (Jinja2 or separate frontend)
│   ├── index.html               # Main page
│
├── database/                    # Database & Migrations
│   ├── schema.sql               # SQL schema (if using raw SQL)
│   ├── seed.py                  # Initial database seeding script
│
├── .env                         # Environment variables (DB credentials, API keys)
├── .gitignore                   # Ignore unnecessary files
├── README.md                    # Project documentation

```

## Getting Started

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd database-setup-project
   ```

2. **Install dependencies:**
   Make sure you have Python and pip installed. Then run:
   ```
   pip install -r ./backend/requirements.txt
   ```

3. **Set up the database:**
   Configure your database settings in `backend/app/config.py`. Ensure that the database server is running.

4. **Run the application:**
   Start the Flask application by executing:
   ```
   python backend/main.py
   ```

5. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000/` to see the welcome message.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is licensed under the MIT License.
