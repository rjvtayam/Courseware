from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio, db
from app.models import Notification, User, Course
from datetime import datetime

def join_user_rooms(user):
    """Helper function to join user to their rooms"""
    try:
        # Join user's personal room
        join_room(f'user_{user.id}')
        
        # Join rooms for all courses user is enrolled in
        if hasattr(user, 'courses_enrolled'):
            for course in user.courses_enrolled:
                join_room(f'course_{course.id}')
        
        # Join rooms for all courses user is teaching
        if hasattr(user, 'courses_teaching'):
            for course in user.courses_teaching:
                join_room(f'course_{course.id}')
                
        return True
    except Exception as e:
        print(f"Error joining rooms for user {user.id}: {str(e)}")
        return False

def leave_user_rooms(user):
    """Helper function to remove user from their rooms"""
    try:
        # Leave user's personal room
        leave_room(f'user_{user.id}')
        
        # Leave rooms for all courses user is enrolled in
        if hasattr(user, 'courses_enrolled'):
            for course in user.courses_enrolled:
                leave_room(f'course_{course.id}')
        
        # Leave rooms for all courses user is teaching
        if hasattr(user, 'courses_teaching'):
            for course in user.courses_teaching:
                leave_room(f'course_{course.id}')
                
        return True
    except Exception as e:
        print(f"Error leaving rooms for user {user.id}: {str(e)}")
        return False

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    try:
        if current_user.is_authenticated:
            success = join_user_rooms(current_user)
            if success:
                # Notify user of successful connection
                emit('connection_status', {
                    'status': 'connected',
                    'user_id': current_user.id,
                    'timestamp': datetime.utcnow().isoformat()
                })
            return success
    except Exception as e:
        print(f"Error in handle_connect: {str(e)}")
        return False

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    try:
        if current_user.is_authenticated:
            success = leave_user_rooms(current_user)
            if success:
                # Notify user of disconnection
                emit('connection_status', {
                    'status': 'disconnected',
                    'user_id': current_user.id,
                    'timestamp': datetime.utcnow().isoformat()
                })
            return success
    except Exception as e:
        print(f"Error in handle_disconnect: {str(e)}")
        return False
