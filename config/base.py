# config/base.py
import os

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secure_secret_key')
    DEBUG = False
    TESTING = False

    # Database Configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'qr')

    # Camera Configuration
    CAMERA_INDEX = int(os.environ.get('CAMERA_INDEX', 0))

    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}