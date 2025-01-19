from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio
from app.models import Notification, User, Course

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        # Join user's personal room
        join_room(f'user_{current_user.id}')
        # Join rooms for all courses user is enrolled in or teaching
        for course in current_user.courses_enrolled:
            join_room(f'course_{course.id}')
        for course in current_user.courses_teaching:
            join_room(f'course_{course.id}')

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        leave_room(f'user_{current_user.id}')
        for course in current_user.courses_enrolled:
            leave_room(f'course_{course.id}')
        for course in current_user.courses_teaching:
            leave_room(f'course_{course.id}')
