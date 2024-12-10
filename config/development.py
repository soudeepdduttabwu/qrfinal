# config/development.py
from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True