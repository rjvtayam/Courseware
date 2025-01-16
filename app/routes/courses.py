from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Course, db
from app.forms.courses import CourseForm

bp = Blueprint('courses', __name__)

@bp.route('/')
def index():
    """Show all available courses to everyone"""
    courses = Course.query.all()
    return render_template('courses/dashboard.html', courses=courses)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_teacher:
        flash('Only teachers can create courses.')
        return redirect(url_for('courses.index'))

    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            title=form.title.data,
            description=form.description.data,
            teacher_id=current_user.id
        )
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully!')
        return redirect(url_for('courses.index'))

    return render_template('courses/create.html', form=form)

@bp.route('/<int:id>')
def view(id):
    """View course details - accessible to everyone"""
    course = Course.query.get_or_404(id)
    return render_template('courses/view.html', course=course)