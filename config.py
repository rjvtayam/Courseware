from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # Handle PostgreSQL Database URL from Render
    DATABASE_URL = environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Render provides postgres:// but SQLAlchemy requires postgresql://
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback for local development
        SQLALCHEMY_DATABASE_URI = 'postgresql://courseware_owner:6UoVsM2NizTk@ep-noisy-darkness-a5ut3d68.us-east-2.aws.neon.tech/courseware?sslmode=require'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = path.join(basedir, 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Elasticsearch configuration
    ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL')