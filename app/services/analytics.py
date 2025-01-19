from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models.analytics import StudentEngagement, LearningActivity, CourseAnalytics
from app.models.models import User, Course, CourseContent, Assignment, Grade

class AnalyticsService:
    @staticmethod
    def track_learning_activity(student_id, course_id, activity_type, duration, 
                              content_id=None, assignment_id=None):
        """Track a single learning activity"""
        activity = LearningActivity(
            student_id=student_id,
            course_id=course_id,
            content_id=content_id,
            assignment_id=assignment_id,
            activity_type=activity_type,
            duration=duration
        )
        
        # Update student engagement metrics
        engagement = StudentEngagement.query.filter_by(
            student_id=student_id,
            course_id=course_id
        ).first()
        
        if not engagement:
            engagement = StudentEngagement(
                student_id=student_id,
                course_id=course_id
            )
            db.session.add(engagement)
        
        engagement.total_time_spent += duration
        engagement.last_activity = datetime.utcnow()
        
        if activity_type == 'view':
            engagement.material_view_count += 1
        elif activity_type == 'submit':
            engagement.assignment_submission_count += 1
        elif activity_type == 'comment':
            engagement.comment_count += 1
            
        db.session.add(activity)
        db.session.commit()
        
        # Update course analytics
        AnalyticsService.update_course_analytics(course_id)
        
        return activity

    @staticmethod
    def get_student_progress(student_id, course_id):
        """Get detailed progress for a student in a course"""
        engagement = StudentEngagement.query.filter_by(
            student_id=student_id,
            course_id=course_id
        ).first()
        
        if not engagement:
            return None
            
        return {
            'total_time_spent': engagement.total_time_spent,
            'material_views': engagement.material_view_count,
            'assignments_completed': engagement.assignments_completed,
            'average_grade': engagement.average_grade,
            'last_activity': engagement.last_activity,
            'engagement_level': AnalyticsService._calculate_engagement_level(engagement)
        }

    @staticmethod
    def get_course_analytics(course_id):
        """Get overall analytics for a course"""
        analytics = CourseAnalytics.query.filter_by(course_id=course_id).first()
        
        if not analytics:
            return None
            
        return {
            'total_students': analytics.total_students,
            'active_students': analytics.active_students,
            'average_engagement_time': analytics.average_engagement_time,
            'content_completion_rate': analytics.average_content_completion,
            'average_grade': analytics.average_grade,
            'submission_rate': (analytics.total_submissions / analytics.total_assignments 
                              if analytics.total_assignments > 0 else 0)
        }

    @staticmethod
    def get_student_engagement_metrics(course_id):
        """Get engagement metrics for all students in a course"""
        engagements = StudentEngagement.query.filter_by(course_id=course_id).all()
        return [{
            'student_id': e.student_id,
            'student_name': e.student.full_name,
            'total_time': e.total_time_spent,
            'last_active': e.last_activity,
            'engagement_level': AnalyticsService._calculate_engagement_level(e),
            'performance': e.average_grade
        } for e in engagements]

    @staticmethod
    def update_course_analytics(course_id):
        """Update analytics for a course"""
        analytics = CourseAnalytics.query.filter_by(course_id=course_id).first()
        if not analytics:
            analytics = CourseAnalytics(course_id=course_id)
            db.session.add(analytics)
        
        # Update student counts
        analytics.total_students = db.session.query(func.count(StudentEngagement.id))\
            .filter_by(course_id=course_id).scalar()
            
        week_ago = datetime.utcnow() - timedelta(days=7)
        analytics.active_students = db.session.query(func.count(StudentEngagement.id))\
            .filter(StudentEngagement.course_id == course_id,
                   StudentEngagement.last_activity >= week_ago).scalar()
        
        # Update engagement metrics
        engagements = StudentEngagement.query.filter_by(course_id=course_id).all()
        if engagements:
            analytics.average_engagement_time = sum(e.total_time_spent for e in engagements) / len(engagements)
        
        # Update grade metrics
        grades = Grade.query.join(Assignment)\
            .filter(Assignment.course_id == course_id).all()
        if grades:
            analytics.average_grade = sum(g.score for g in grades) / len(grades)
        
        analytics.updated_at = datetime.utcnow()
        db.session.commit()
        return analytics

    @staticmethod
    def _calculate_engagement_level(engagement):
        """Calculate engagement level based on various metrics"""
        # This is a simple scoring system - can be made more sophisticated
        score = 0
        
        # Time spent
        if engagement.total_time_spent > 3600:  # More than 1 hour
            score += 3
        elif engagement.total_time_spent > 1800:  # More than 30 minutes
            score += 2
        elif engagement.total_time_spent > 600:  # More than 10 minutes
            score += 1
            
        # Material views
        if engagement.material_view_count > 10:
            score += 3
        elif engagement.material_view_count > 5:
            score += 2
        elif engagement.material_view_count > 0:
            score += 1
            
        # Assignment submissions
        if engagement.assignment_submission_count > 5:
            score += 3
        elif engagement.assignment_submission_count > 2:
            score += 2
        elif engagement.assignment_submission_count > 0:
            score += 1
            
        # Comments
        if engagement.comment_count > 5:
            score += 3
        elif engagement.comment_count > 2:
            score += 2
        elif engagement.comment_count > 0:
            score += 1
            
        # Convert score to level
        if score >= 10:
            return 'High'
        elif score >= 5:
            return 'Medium'
        return 'Low'
