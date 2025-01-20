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
    
    # Debug print for database URL
    print("Database URL in create_app:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    # Ensure we're using PostgreSQL
    if not (app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql://') or 
            app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://')):
        print("ERROR: Invalid database URL format:", app.config['SQLALCHEMY_DATABASE_URI'])
        raise ValueError(f"Database must be PostgreSQL. Current URL: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Convert postgres:// to postgresql:// if needed
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
        print("Converted database URL:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, 
                     cors_allowed_origins="*",
                     manage_session=False,
                     ping_timeout=60,
                     ping_interval=25)
    
    # Initialize Elasticsearch if configured
    global elasticsearch
    if app.config.get('ELASTICSEARCH_URL'):
        elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])

    # Register blueprints and initialize models
    with app.app_context():
        # Import models
        from app.models.models import User, Course, Assignment, Feedback, Grade, Notification, Comment
        
        # Test database connection with retries
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                db.engine.connect()
                # Create all database tables
                db.create_all()
                break
            except Exception as e:
                retry_count += 1
                print(f"Database connection attempt {retry_count} failed: {str(e)}")
                if retry_count == max_retries:
                    raise
                import time
                time.sleep(1)  # Wait 1 second before retrying
        
        # Import and register blueprints
        from app.routes import (
            main, auth, courses, assignments, resources, 
            workspace, search, notifications, feedback
        )
        
        # Core blueprints
        app.register_blueprint(main.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(courses.bp)
        app.register_blueprint(assignments.bp)
        app.register_blueprint(resources.bp)
        app.register_blueprint(workspace.bp)
        
        # Additional feature blueprints
        app.register_blueprint(search.bp)
        app.register_blueprint(notifications.bp)
        app.register_blueprint(feedback.bp)

    return app
