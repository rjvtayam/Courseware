from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import Course, User, CourseContent, Assignment
from app import db

bp = Blueprint('workspace', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    """Main workspace dashboard showing courses and activities"""
    if current_user.is_teacher:
        # Get courses where user is the instructor
        courses = Course.query.filter_by(instructor_id=current_user.id).all()
        teaching = True
    else:
        # Get courses where user is enrolled
        courses = current_user.courses_enrolled
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
            instructor_id=current_user.id
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
    if not (current_user.id == course.instructor_id or course in current_user.courses_enrolled):
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
    
    if current_user.id != course.instructor_id:
        flash("Only the course instructor can add content.", "error")
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
    
    if current_user.id != course.instructor_id:
        flash("Only the course instructor can add assignments.", "error")
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
