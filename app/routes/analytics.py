from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from app.services.analytics import AnalyticsService

analytics = Blueprint('analytics', __name__)

@analytics.route('/analytics/course/<int:course_id>')
@login_required
def course_analytics(course_id):
    """Course analytics dashboard"""
    if not current_user.is_teacher:
        return jsonify({'error': 'Unauthorized'}), 403
        
    return render_template('analytics/dashboard.html', course_id=course_id)

@analytics.route('/api/analytics/course/<int:course_id>')
@login_required
def get_course_analytics(course_id):
    """Get course analytics data"""
    if not current_user.is_teacher:
        return jsonify({'error': 'Unauthorized'}), 403
        
    analytics = AnalyticsService.get_course_analytics(course_id)
    engagement = AnalyticsService.get_student_engagement_metrics(course_id)
    
    return jsonify({
        'course_analytics': analytics,
        'student_engagement': engagement
    })

@analytics.route('/api/analytics/student/<int:student_id>/course/<int:course_id>')
@login_required
def get_student_analytics(student_id, course_id):
    """Get detailed analytics for a student"""
    if not current_user.is_teacher:
        return jsonify({'error': 'Unauthorized'}), 403
        
    progress = AnalyticsService.get_student_progress(student_id, course_id)
    
    if not progress:
        return jsonify({'error': 'No data found'}), 404
        
    return jsonify(progress)
