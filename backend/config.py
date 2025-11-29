import os

class Config:
    SECRET_KEY = "your-secret-key-change-in-prod"

    SQLALCHEMY_DATABASE_URI = "sqlite:///parking.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis Cache
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/1"

    # Celery Configuration
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

    # For auto-discovering Celery tasks
    CELERY_IMPORTS = ["tasks"]   
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "parthtiwari2599@gmail.com"
    MAIL_PASSWORD = "pass123"   
    
