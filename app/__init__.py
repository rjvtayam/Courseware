from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from elasticsearch import Elasticsearch
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
socketio = SocketIO()
elasticsearch = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure we're using PostgreSQL
    if not app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql://'):
        raise ValueError("Database must be PostgreSQL")

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Initialize Elasticsearch if configured
    global elasticsearch
    if app.config.get('ELASTICSEARCH_URL'):
        elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])

    with app.app_context():
        # Import models
        from app.models.models import User, Course, Assignment, Feedback, Grade, Notification, Comment
        
        # Create all database tables
        db.create_all()
        
        # Import and register blueprints
        from app.routes import auth, courses, assignments
        app.register_blueprint(auth.bp)
        app.register_blueprint(courses.bp)
        app.register_blueprint(assignments.bp)
        
        from app.routes import feedback, notifications, search, dashboard
        app.register_blueprint(feedback.bp)
        app.register_blueprint(notifications.bp)
        app.register_blueprint(search.bp)
        app.register_blueprint(dashboard.bp)

    return app
