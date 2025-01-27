from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from flask_socketio import emit, join_room, leave_room
from app.models import Notification, Course, User, Enrollment
from app import socketio, db
from datetime import datetime
from sqlalchemy import desc

bp = Blueprint('notifications', __name__)

@bp.route('/api/notifications')
@login_required
def get_notifications():
    """Get paginated notifications for current user"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    unread_only = request.args.get('unread_only', False, type=bool)
    
    query = Notification.query.filter_by(user_id=current_user.id)
    if unread_only:
        query = query.filter_by(is_read=False)
    
    notifications = query.order_by(desc(Notification.created_at))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'notifications': [{
            'id': n.id,
            'message': n.message,
            'type': n.type,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat(),
            'related_id': n.related_id,
            'url': n.get_url() if hasattr(n, 'get_url') else None
        } for n in notifications.items],
        'total': notifications.total,
        'pages': notifications.pages,
        'current_page': notifications.page
    })

@bp.route('/notifications')
@login_required
def notifications_page():
    """Render notifications page"""
    unread_count = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).count()
    return render_template('notifications/index.html', unread_count=unread_count)

@bp.route('/api/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    """Mark all notifications as read for current user"""
    Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_read(notification_id):
    """Mark specific notification as read"""
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    notification.is_read = True
    db.session.commit()
    return jsonify({'success': True})

def send_notification(user_id, message, notification_type, related_id=None, url=None):
    """Send real-time notification to specific user"""
    notification = Notification(
        user_id=user_id,
        message=message,
        type=notification_type,
        related_id=related_id,
        created_at=datetime.utcnow()
    )
    
    if url:
        notification.url = url
        
    db.session.add(notification)
    db.session.commit()
    
    # Emit WebSocket event to specific user
    notification_data = {
        'id': notification.id,
        'message': message,
        'type': notification_type,
        'related_id': related_id,
        'url': url,
        'created_at': notification.created_at.isoformat()
    }
    socketio.emit('notification', notification_data, room=f'user_{user_id}')
    return notification

def send_course_notification(course_id, message, notification_type, exclude_user_id=None, url=None):
    """Send notification to all users in a course"""
    course = Course.query.get_or_404(course_id)
    
    # Get all enrolled students and instructor
    users = [enrollment.student_id for enrollment in course.enrollments]
    users.append(course.teacher_id)
    
    # Remove excluded user if specified
    if exclude_user_id and exclude_user_id in users:
        users.remove(exclude_user_id)
    
    notifications = []
    for user_id in users:
        notification = send_notification(
            user_id=user_id,
            message=message,
            notification_type=notification_type,
            related_id=course_id,
            url=url
        )
        notifications.append(notification)
    
    return notifications

@socketio.on('connect')
def handle_connect(auth=None):
    """Add user to their personal notification room and course rooms"""
    if not current_user.is_authenticated:
        return False
    
    # Join user's personal notification room
    join_room(f'user_{current_user.id}')
    
    # Join course rooms for real-time updates
    if current_user.is_teacher:
        # Teachers join rooms for courses they teach
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
        for course in courses:
            join_room(f'course_{course.id}')
            # Also join the general room for this course
            join_room(f'room_{course.id}')
    else:
        # Students join rooms for courses they're enrolled in
        enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
        for enrollment in enrollments:
            join_room(f'course_{enrollment.course_id}')
            # Also join the general room for this course
            join_room(f'room_{enrollment.course_id}')
    
    return True

@socketio.on('disconnect')
def handle_disconnect(sid=None):
    """Remove user from their rooms on disconnect"""
    if not current_user.is_authenticated:
        return
    
    # Leave user's personal notification room
    leave_room(f'user_{current_user.id}')
    
    # Leave course rooms
    if current_user.is_teacher:
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
    else:
        enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
        courses = [enrollment.course for enrollment in enrollments]
    
    for course in courses:
        leave_room(f'course_{course.id}')
        # Also leave the general room for this course
        leave_room(f'room_{course.id}')

@socketio.on('join')
def on_join(data):
    if current_user.is_authenticated:
        course_id = data.get('course_id')
        if course_id:
            course = Course.query.get(course_id)
            if course:
                # Check if user is enrolled or is the teacher
                is_enrolled = Enrollment.query.filter_by(
                    student_id=current_user.id,
                    course_id=course_id
                ).first() is not None
                
                if is_enrolled or course.teacher_id == current_user.id:
                    room = f'course_{course_id}'
                    socketio.emit('joined_room', {'room': room}, room=room)

@bp.route('/notifications/unread', methods=['GET'])
@login_required
def get_unread_notifications():
    notifications = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).order_by(Notification.created_at.desc()).all()
    
    return jsonify([{
        'id': n.id,
        'message': n.message,
        'type': n.type,
        'created_at': n.created_at.isoformat()
    } for n in notifications])

@bp.route('/notifications/mark_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    notification.is_read = True
    db.session.commit()
    return jsonify({'status': 'success'})

@bp.route('/notifications/mark_all_read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()
    return jsonify({'status': 'success'})