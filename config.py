from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # Handle PostgreSQL Database URL from Render
    DATABASE_URL = environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or \
        'sqlite:///' + path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = path.join(basedir, 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Elasticsearch configuration
    ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'
    
    # WebSocket configuration
    SOCKET_IO_PING_TIMEOUT = 10
    SOCKET_IO_PING_INTERVAL = 25