import os

class Config:
    # SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Use environment variable or fallback
    SECRET_KEY = "your_secret_key_here"  # Ensure secret key is set
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
