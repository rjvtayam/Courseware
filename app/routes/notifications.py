from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from flask_socketio import emit
from app.models import Notification, db
from app import socketio

bp = Blueprint('notifications', __name__)

@bp.route('/notifications')
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).order_by(Notification.created_at.desc()).all()
    return render_template('notifications/index.html', notifications=notifications)

@bp.route('/notifications/mark-read/<int:id>', methods=['POST'])
@login_required
def mark_read(id):
    notification = Notification.query.get_or_404(id)
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    notification.is_read = True
    db.session.commit()
    return jsonify({'success': True})

def send_notification(user_id, message, notification_type):
    """Send real-time notification to specific user"""
    notification = Notification(
        user_id=user_id,
        message=message,
        type=notification_type
    )
    db.session.add(notification)
    db.session.commit()
    
    # Emit WebSocket event to specific user
    socketio.emit('new_notification', 
                 {'id': notification.id, 
                  'message': message, 
                  'type': notification_type},
                 room=f'user_{user_id}')

@socketio.on('connect')
@login_required
def handle_connect():
    """Add user to their personal room for targeted notifications"""
    socketio.join_room(f'user_{current_user.id}')