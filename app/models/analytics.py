from datetime import datetime
from app import db

class StudentEngagement(db.Model):
    """Track detailed student engagement metrics"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Time tracking
    total_time_spent = db.Column(db.Integer, default=0)  # in seconds
    last_activity = db.Column(db.DateTime)
    
    # Engagement metrics
    login_count = db.Column(db.Integer, default=0)
    material_view_count = db.Column(db.Integer, default=0)
    assignment_submission_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    
    # Performance metrics
    assignments_completed = db.Column(db.Integer, default=0)
    average_grade = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', backref=db.backref('engagement_metrics', lazy=True))
    course = db.relationship('Course', backref=db.backref('student_engagement', lazy=True))

class LearningActivity(db.Model):
    """Track individual learning activities"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('course_content.id'), nullable=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=True)
    
    activity_type = db.Column(db.String(50))  # 'view', 'submit', 'comment', etc.
    duration = db.Column(db.Integer)  # Time spent in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student = db.relationship('User', backref=db.backref('learning_activities', lazy=True))
    course = db.relationship('Course', backref=db.backref('learning_activities', lazy=True))
    content = db.relationship('CourseContent', backref=db.backref('learning_activities', lazy=True))
    assignment = db.relationship('Assignment', backref=db.backref('learning_activities', lazy=True))

class CourseAnalytics(db.Model):
    """Track overall course analytics"""
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Engagement metrics
    total_students = db.Column(db.Integer, default=0)
    active_students = db.Column(db.Integer, default=0)  # Active in last 7 days
    average_engagement_time = db.Column(db.Float, default=0.0)  # Average time per student
    
    # Content metrics
    total_content_views = db.Column(db.Integer, default=0)
    average_content_completion = db.Column(db.Float, default=0.0)
    
    # Assignment metrics
    total_assignments = db.Column(db.Integer, default=0)
    total_submissions = db.Column(db.Integer, default=0)
    average_grade = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = db.relationship('Course', backref=db.backref('analytics', uselist=False))
