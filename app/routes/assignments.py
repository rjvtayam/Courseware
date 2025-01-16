from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from app.models import Assignment, Submission, Comment, Course, db
from app.forms.assignments import AssignmentForm, SubmissionForm, CommentForm

bp = Blueprint('assignments', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'zip'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/course/<int:course_id>/assignments/create', methods=['GET', 'POST'])
@login_required
def create(course_id):
    if not current_user.is_teacher:
        flash('Only teachers can create assignments.')
        return redirect(url_for('courses.view', id=course_id))
    
    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(
            title=form.title.data,
            description=form.description.data,
            course_id=course_id,
            due_date=form.due_date.data
        )
        
        # Handle file upload for assignment materials
        if form.materials.data:
            file = form.materials.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'materials', filename)
                file.save(filepath)
                assignment.material_path = f'materials/{filename}'
        
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment created successfully!')
        return redirect(url_for('courses.view', id=course_id))
    
    return render_template('assignments/create.html', form=form, course_id=course_id)

@bp.route('/assignments/<int:id>', methods=['GET', 'POST'])
def view(id):
    assignment = Assignment.query.get_or_404(id)
    submission_form = SubmissionForm()
    comment_form = CommentForm()
    
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please login to submit assignments or comment.')
            return redirect(url_for('auth.login'))
        
        if 'submit_work' in request.form and submission_form.validate():
            file = submission_form.file.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'submissions', filename)
                file.save(filepath)
                
                submission = Submission(
                    student_id=current_user.id,
                    assignment_id=id,
                    file_path=f'submissions/{filename}'
                )
                db.session.add(submission)
                db.session.commit()
                flash('Work submitted successfully!')
            
        elif 'add_comment' in request.form and comment_form.validate():
            comment = Comment(
                content=comment_form.content.data,
                user_id=current_user.id,
                assignment_id=id
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment added successfully!')
            
    submissions = Submission.query.filter_by(assignment_id=id).all()
    comments = Comment.query.filter_by(assignment_id=id).order_by(Comment.created_at.desc()).all()
    
    return render_template('assignments/view.html',
                         assignment=assignment,
                         submission_form=submission_form,
                         comment_form=comment_form,
                         submissions=submissions,
                         comments=comments)