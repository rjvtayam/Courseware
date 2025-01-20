from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.models import Course, User, CourseContent, Assignment
from app import db, socketio
from flask_socketio import join_room, leave_room, emit
from datetime import datetime

bp = Blueprint('workspace', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    """Main workspace dashboard showing courses and activities"""
    if current_user.is_teacher:
        # Get courses where user is the teacher
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
        teaching = True
    else:
        # Show all available courses to students
        courses = Course.query.all()
        teaching = False
    
    return render_template('workspace/dashboard.html',
                         courses=courses,
                         teaching=teaching)

@bp.route('/course/create', methods=['GET', 'POST'])
@login_required
def create_course():
    """Create a new course (teachers only)"""
    if not current_user.is_teacher:
        flash("Only teachers can create courses.", "error")
        return redirect(url_for('workspace.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash("Course title is required.", "error")
            return redirect(url_for('workspace.create_course'))
        
        course = Course(
            title=title,
            description=description,
            teacher_id=current_user.id
        )
        db.session.add(course)
        db.session.commit()
        
        flash(f"Course '{title}' has been created successfully!", "success")
        return redirect(url_for('workspace.course', course_id=course.id))
    
    return render_template('workspace/create_course.html')

@bp.route('/course/<int:course_id>')
@login_required
def course(course_id):
    """View course details and content"""
    course = Course.query.get_or_404(course_id)
    
    # Check if user has access to this course
    if not (current_user.id == course.teacher_id or course in current_user.courses_enrolled):
        flash("You don't have access to this course.", "error")
        return redirect(url_for('workspace.dashboard'))
    
    contents = CourseContent.query.filter_by(course_id=course_id)\
        .order_by(CourseContent.order).all()
    assignments = Assignment.query.filter_by(course_id=course_id)\
        .order_by(Assignment.due_date).all()
    
    return render_template('workspace/course.html',
                         course=course,
                         contents=contents,
                         assignments=assignments)

@bp.route('/course/<int:course_id>/content/add', methods=['GET', 'POST'])
@login_required
def add_content(course_id):
    """Add content to a course (teachers only)"""
    course = Course.query.get_or_404(course_id)
    
    if current_user.id != course.teacher_id:
        flash("Only the course teacher can add content.", "error")
        return redirect(url_for('workspace.course', course_id=course_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        content_type = request.form.get('type')
        file_id = request.form.get('file_id')  # From Google Drive or similar
        
        if not all([title, content_type, file_id]):
            flash("Please fill in all required fields.", "error")
            return redirect(url_for('workspace.add_content', course_id=course_id))
        
        content = CourseContent(
            title=title,
            description=description,
            course_id=course_id,
            content_type=content_type,
            drive_file_id=file_id,
            order=len(course.contents) + 1
        )
        db.session.add(content)
        db.session.commit()
        
        flash("Content has been added successfully!", "success")
        return redirect(url_for('workspace.course', course_id=course_id))
    
    return render_template('workspace/add_content.html', course=course)

@bp.route('/course/<int:course_id>/assignment/add', methods=['GET', 'POST'])
@login_required
def add_assignment(course_id):
    """Add assignment to a course (teachers only)"""
    course = Course.query.get_or_404(course_id)
    
    if current_user.id != course.teacher_id:
        flash("Only the course teacher can add assignments.", "error")
        return redirect(url_for('workspace.course', course_id=course_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        
        if not all([title, description, due_date]):
            flash("Please fill in all required fields.", "error")
            return redirect(url_for('workspace.add_assignment', course_id=course_id))
        
        assignment = Assignment(
            title=title,
            description=description,
            course_id=course_id,
            due_date=due_date
        )
        db.session.add(assignment)
        db.session.commit()
        
        flash("Assignment has been added successfully!", "success")
        return redirect(url_for('workspace.course', course_id=course_id))
    
    return render_template('workspace/add_assignment.html', course=course)

@bp.route('/course/<int:course_id>/materials')
@login_required
def course_materials(course_id):
    """View and manage course materials"""
    course = Course.query.get_or_404(course_id)
    
    # Check if user has access to this course
    if not (current_user.id == course.teacher_id or course in current_user.courses_enrolled):
        flash("You don't have access to this course.", "error")
        return redirect(url_for('workspace.dashboard'))
    
    materials = CourseContent.query.filter_by(
        course_id=course_id,
        content_type='material'
    ).order_by(CourseContent.order).all()
    
    return render_template('workspace/materials.html',
                         course=course,
                         materials=materials)

@bp.route('/course/<int:course_id>/materials/upload', methods=['POST'])
@login_required
def upload_material(course_id):
    """Upload material to a course"""
    course = Course.query.get_or_404(course_id)
    
    if current_user.id != course.teacher_id:
        return jsonify({'error': 'Only the course teacher can upload materials'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Save file to Google Drive
        file_metadata = {
            'name': file.filename,
            'parents': [course.material_folder_id]
        }
        media = MediaFileUpload(file, resumable=True)
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        # Create material record
        material = CourseContent(
            title=file.filename,
            description=request.form.get('description', ''),
            course_id=course_id,
            content_type='material',
            drive_file_id=file['id'],
            order=len(course.contents) + 1
        )
        db.session.add(material)
        db.session.commit()
        
        # Notify course members
        emit('material_uploaded', {
            'course_id': course_id,
            'material_id': material.id,
            'title': material.title
        }, room=f'course_{course_id}')
        
        return jsonify({'success': True, 'material_id': material.id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/course/<int:course_id>/room')
@login_required
def course_room(course_id):
    """View course room with chat and materials"""
    course = Course.query.get_or_404(course_id)
    
    # Check if user has access to this course
    if not (current_user.id == course.teacher_id or course in current_user.courses_enrolled):
        flash("You don't have access to this course.", "error")
        return redirect(url_for('workspace.dashboard'))
    
    return render_template('workspace/room.html', course=course)

# WebSocket event handlers for course rooms
@socketio.on('join_course_room')
def handle_join_room(data):
    """Join a course room"""
    course_id = data.get('course_id')
    if not course_id:
        return False
    
    course = Course.query.get(course_id)
    if not course:
        return False
    
    # Verify user has access to this course
    if not (current_user.id == course.teacher_id or course in current_user.courses_enrolled):
        return False
    
    room = f'course_{course_id}'
    join_room(room)
    
    # Notify others in the room
    emit('user_joined', {
        'user_id': current_user.id,
        'username': current_user.username,
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)
    
    return True

@socketio.on('leave_course_room')
def handle_leave_room(data):
    """Leave a course room"""
    course_id = data.get('course_id')
    if not course_id:
        return False
    
    room = f'course_{course_id}'
    leave_room(room)
    
    # Notify others in the room
    emit('user_left', {
        'user_id': current_user.id,
        'username': current_user.username,
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)
    
    return True

@socketio.on('course_message')
def handle_course_message(data):
    """Handle course room messages"""
    course_id = data.get('course_id')
    message = data.get('message')
    
    if not course_id or not message:
        return False
    
    course = Course.query.get(course_id)
    if not course:
        return False
    
    # Verify user has access to this course
    if not (current_user.id == course.teacher_id or course in current_user.courses_enrolled):
        return False
    
    # Broadcast message to room
    emit('room_message', {
        'user_id': current_user.id,
        'username': current_user.username,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }, room=f'course_{course_id}')
    
    return True
