from flask import Blueprint, render_template
from flask_login import current_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('welcome.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
