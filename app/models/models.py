from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # OAuth fields
    google_id = db.Column(db.String(120), unique=True, nullable=True)
    github_id = db.Column(db.String(120), unique=True, nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)  # Profile picture URL
    oauth_provider = db.Column(db.String(20), nullable=True)  # 'google' or 'github'
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_teacher = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    courses_teaching = db.relationship('Course', backref='teacher', lazy='dynamic')
    courses_enrolled = db.relationship('Course', secondary='enrollment',
                                     backref=db.backref('students', lazy='dynamic'))
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    feedback_given = db.relationship('Feedback', backref='teacher', lazy='dynamic',
                                   foreign_keys='Feedback.teacher_id')
    grades = db.relationship('Grade', backref='student', lazy='dynamic')
    user_comments = db.relationship('Comment', backref='author', lazy='dynamic')
    progress = db.relationship('CourseProgress', lazy='dynamic')

    @property
    def full_name(self):
        return self.username

    def get_content_progress(self, content_id):
        """Get progress for specific content"""
        progress = CourseProgress.query.filter_by(
            user_id=self.id,
            content_id=content_id
        ).first()
        return progress

    def mark_content_viewed(self, content_id):
        """Mark content as viewed and update progress"""
        progress = self.get_content_progress(content_id)
        if not progress:
            progress = CourseProgress(
                user_id=self.id,
                content_id=content_id
            )
            db.session.add(progress)
        
        progress.last_viewed = datetime.utcnow()
        progress.view_count += 1
        db.session.commit()
        return progress

    def mark_content_completed(self, content_id):
        """Mark content as completed"""
        progress = self.get_content_progress(content_id)
        if not progress:
            progress = CourseProgress(
                user_id=self.id,
                content_id=content_id
            )
            db.session.add(progress)
        
        progress.completed = True
        progress.last_viewed = datetime.utcnow()
        db.session.commit()
        return progress

    def get_course_progress(self, course_id):
        """Get overall progress for a course"""
        course = Course.query.get(course_id)
        if not course:
            return 0
        
        total_content = len(course.contents)
        if total_content == 0:
            return 100  # No content means course is complete
            
        completed = CourseProgress.query.join(CourseContent).filter(
            CourseProgress.user_id == self.id,
            CourseContent.course_id == course_id,
            CourseProgress.completed == True
        ).count()
        
        return (completed / total_content) * 100

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=True) 
    video_folder_id = db.Column(db.String(100)) 
    material_folder_id = db.Column(db.String(100)) 
    
    # Relationships
    assignments = db.relationship('Assignment', backref='course', lazy='dynamic')
    contents = db.relationship('CourseContent', back_populates='course', lazy='dynamic')
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic')

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    materials_path = db.Column(db.String(255))
    
    # Relationships
    submissions = db.relationship('Submission', backref='assignment', lazy='dynamic')
    assignment_comments = db.relationship('Comment', backref='assignment', lazy='dynamic')

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with Feedback
    feedback = db.relationship('Feedback', backref='submission', lazy='dynamic')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)  # Added foreign key
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CourseContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    content_type = db.Column(db.String(50))  # 'video', 'document', 'link', 'text'
    drive_file_id = db.Column(db.String(100))  # For uploaded files (videos, documents)
    drive_view_link = db.Column(db.String(255))  # For files and external links
    text_content = db.Column(db.Text)  # For text tutorials
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course = db.relationship('Course', back_populates='contents')
    progress = db.relationship('CourseProgress', backref='content_item', lazy=True)

    def to_dict(self):
        """Convert content to dictionary format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content_type': self.content_type,
            'drive_view_link': self.drive_view_link,
            'text_content': self.text_content,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CourseProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('course_content.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    last_viewed = db.Column(db.DateTime)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))