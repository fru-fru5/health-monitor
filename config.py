import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:fru23junior01.05%23@localhost/health_monitor'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
