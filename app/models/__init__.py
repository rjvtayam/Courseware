from .models import User, Course, Assignment, Enrollment, Notification, Feedback, Grade, Submission, Comment

# Make models available at package level
User = User
Course = Course
Assignment = Assignment
Enrollment = Enrollment
Notification = Notification
Feedback = Feedback
Grade = Grade
Submission = Submission
Comment = Comment

__all__ = ['User', 'Course', 'Assignment', 'Enrollment', 'Notification', 'Feedback', 'Grade', 'Submission', 'Comment']
