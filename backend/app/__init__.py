from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import db
from .config import Config

def create_app():
    app = Flask(__name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
    app.config.from_object(Config)

    # Initialize extensions
    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register Blueprints
    from .routes import main_bp
    from .auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
