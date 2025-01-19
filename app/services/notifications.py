from flask_socketio import emit
from app import db
from app.models import Notification, User, Course
from datetime import datetime

def send_notification(user_id, message, notification_type, related_id=None):
    """
    Send a notification to a specific user
    """
    notification = Notification(
        user_id=user_id,
        message=message,
        type=notification_type,
        related_id=related_id,
        created_at=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()
    
    # Emit real-time notification
    emit('notification', {
        'id': notification.id,
        'message': message,
        'type': notification_type,
        'related_id': related_id,
        'created_at': notification.created_at.isoformat()
    }, room=f'user_{user_id}')

def send_course_notification(course_id, message, notification_type, exclude_user_id=None):
    """
    Send a notification to all users in a course
    """
    course = Course.query.get(course_id)
    if not course:
        return
    
    # Get all users in the course (both students and teacher)
    users = [enrollment.student_id for enrollment in course.enrollments]
    users.append(course.instructor_id)
    
    # Remove excluded user if specified
    if exclude_user_id and exclude_user_id in users:
        users.remove(exclude_user_id)
    
    # Send notification to each user
    for user_id in users:
        send_notification(user_id, message, notification_type, related_id=course_id)

def mark_notification_read(notification_id, user_id):
    """
    Mark a notification as read
    """
    notification = Notification.query.filter_by(
        id=notification_id, 
        user_id=user_id
    ).first()
    
    if notification:
        notification.is_read = True
        db.session.commit()
        return True
    return False

def get_user_notifications(user_id, limit=20, offset=0, unread_only=False):
    """
    Get notifications for a user
    """
    query = Notification.query.filter_by(user_id=user_id)
    if unread_only:
        query = query.filter_by(is_read=False)
    
    return query.order_by(Notification.created_at.desc())\
                .offset(offset)\
                .limit(limit)\
                .all()
