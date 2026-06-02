import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Flask configuration using environment variables with safe defaults."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-for-tests')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@wailsalutem.nl')
    API_URL = os.environ.get('API_URL')
    API_KEY = os.environ.get('API_KEY')
    DATABASE = os.environ.get('DATABASE')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:changeme@db:3306/Workshopportaal'
    ).strip()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    }
    WTF_CSRF_ENABLED = True
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
