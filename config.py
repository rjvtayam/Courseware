from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # Handle PostgreSQL Database URL from Render
    DATABASE_URL = environ.get('DATABASE_URL')
    print("Raw DATABASE_URL from environment:", DATABASE_URL)  # Debug print
    
    # Default PostgreSQL URL for production
    DEFAULT_POSTGRES_URL = 'postgresql://courseware_owner:6UoVsM2NizTk@ep-noisy-darkness-a5ut3d68.us-east-2.aws.neon.tech/courseware?sslmode=require'
    
    if DATABASE_URL:
        # Check if it's a MySQL URL
        if DATABASE_URL.startswith('mysql://'):
            print("Converting MySQL URL to PostgreSQL URL")  # Debug print
            SQLALCHEMY_DATABASE_URI = DEFAULT_POSTGRES_URL
        else:
            # Render provides postgres:// but SQLAlchemy requires postgresql://
            if DATABASE_URL.startswith('postgres://'):
                DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
                print("Modified DATABASE_URL:", DATABASE_URL)  # Debug print
            elif DATABASE_URL.startswith('postgresql://'):
                print("URL already in correct format:", DATABASE_URL)  # Debug print
            else:
                print("WARNING: Using default PostgreSQL URL")  # Debug print
                DATABASE_URL = DEFAULT_POSTGRES_URL
            SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        print("No DATABASE_URL found in environment, using default PostgreSQL URL")  # Debug print
        SQLALCHEMY_DATABASE_URI = DEFAULT_POSTGRES_URL
    
    print("Final SQLALCHEMY_DATABASE_URI:", SQLALCHEMY_DATABASE_URI)  # Debug print
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = path.join(basedir, 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Elasticsearch configuration
    ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL')

    # OAuth Configuration
    GOOGLE_CLIENT_ID = environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = environ.get('GOOGLE_DISCOVERY_URL', 'https://accounts.google.com/.well-known/openid-configuration')
    
    GITHUB_CLIENT_ID = environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = environ.get('GITHUB_CLIENT_SECRET')