from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Submission, Feedback, Notification
from app import db

bp = Blueprint('feedback', __name__)

@bp.route('/submission/<int:submission_id>/feedback', methods=['POST'])
@login_required
def add_feedback(submission_id):
    if not current_user.is_teacher:
        flash('Only teachers can provide feedback.')
        return redirect(url_for('assignments.view', id=submission_id))
    
    submission = Submission.query.get_or_404(submission_id)
    feedback = Feedback(
        submission_id=submission_id,
        teacher_id=current_user.id,
        content=request.form.get('feedback'),
        grade=request.form.get('grade')
    )
    
    # Create notification for the student
    notification = Notification(
        user_id=submission.student_id,
        content=f'New feedback received for {submission.assignment.title}',
        link=url_for('assignments.view', id=submission.assignment_id)
    )
    
    db.session.add(feedback)
    db.session.add(notification)
    db.session.commit()
    
    flash('Feedback provided successfully!')
    return redirect(url_for('assignments.view', id=submission.assignment_id))
