# config/production.py
from .base import BaseConfig

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False