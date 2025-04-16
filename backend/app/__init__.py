import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from .models import db
from .config import Config

def create_app():
    # Ensure correct paths for templates and static files
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    template_path = os.path.join(BASE_DIR, '../../frontend/templates')
    static_path = os.path.join(BASE_DIR, '../../frontend/static')

    app = Flask(__name__, template_folder=template_path, static_folder=static_path)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Ensure secret key is set

    # Initialize extensions
    CORS(app)  # Enable CORS with credentials support
    db.init_app(app)

    with app.app_context():  
        db.create_all()


    csrf = CSRFProtect(app)


    # Register Blueprints
    from .routes import main_bp
    from .auth import auth_bp
    from .supervisor_routes import supervisor_bp
    from .resident_routes import resident_bp
    from .clerk_routes import clerk_bp
    from .admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth") # Prefix auth routes
    app.register_blueprint(supervisor_bp, url_prefix="/supervisor")  # Prefix supervisor routes
    app.register_blueprint(resident_bp, url_prefix="/resident")  # Prefix resident routes
    app.register_blueprint(clerk_bp, url_prefix="/clerk")  # Prefix clerk routes
    app.register_blueprint(admin_bp, url_prefix="/admin")  # Prefix admin routes
    return app
