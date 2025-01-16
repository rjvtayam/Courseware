from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models import Course, Assignment, User, Feedback, Grade
from app import db, socketio

bp = Blueprint('dashboard', __name__)

@bp.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    if not current_user.is_teacher:
        return redirect(url_for('main.index'))
    
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    return render_template('dashboard/teacher.html', courses=courses)

@bp.route('/teacher/course/<int:course_id>/analytics')
@login_required
def course_analytics(course_id):
    if not current_user.is_teacher:
        return redirect(url_for('main.index'))
    
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get course analytics
    total_students = course.students.count()
    assignments = Assignment.query.filter_by(course_id=course_id).all()
    
    # Calculate average grades and completion rates
    analytics = {
        'total_students': total_students,
        'assignments': [],
        'overall_average': 0,
        'completion_rate': 0
    }
    
    total_grade = 0
    total_completed = 0
    
    for assignment in assignments:
        grades = Grade.query.filter_by(assignment_id=assignment.id).all()
        completed = len(grades)
        avg_grade = sum(g.score for g in grades) / completed if completed > 0 else 0
        
        analytics['assignments'].append({
            'id': assignment.id,
            'title': assignment.title,
            'avg_grade': avg_grade,
            'completion_rate': (completed / total_students * 100) if total_students > 0 else 0
        })
        
        total_grade += avg_grade
        total_completed += completed
    
    if assignments:
        analytics['overall_average'] = total_grade / len(assignments)
        analytics['completion_rate'] = (total_completed / (total_students * len(assignments)) * 100) if total_students > 0 else 0
    
    return jsonify(analytics)

@bp.route('/teacher/feedback/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def manage_feedback(assignment_id):
    if not current_user.is_teacher:
        return redirect(url_for('main.index'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.course.teacher_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        feedback_text = request.form.get('feedback')
        grade = request.form.get('grade', type=float)
        
        # Update or create feedback
        feedback = Feedback.query.filter_by(
            assignment_id=assignment_id,
            student_id=student_id
        ).first()
        
        if not feedback:
            feedback = Feedback(
                assignment_id=assignment_id,
                student_id=student_id,
                teacher_id=current_user.id
            )
            db.session.add(feedback)
        
        feedback.text = feedback_text
        
        # Update or create grade
        grade_entry = Grade.query.filter_by(
            assignment_id=assignment_id,
            student_id=student_id
        ).first()
        
        if not grade_entry:
            grade_entry = Grade(
                assignment_id=assignment_id,
                student_id=student_id
            )
            db.session.add(grade_entry)
        
        grade_entry.score = grade
        db.session.commit()
        
        # Send real-time notification to student
        from app.routes.notifications import send_notification
        send_notification(
            student_id,
            f'New feedback available for {assignment.title}',
            'feedback'
        )
        
        return jsonify({'success': True})
    
    # GET request - return feedback form
    return render_template(
        'dashboard/feedback.html',
        assignment=assignment,
        students=assignment.course.students
    )
