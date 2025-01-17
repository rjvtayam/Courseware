from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.models import Course, User, CourseContent
from app.utils.drive_helper import drive_service
from app import db
import os

bp = Blueprint('courses', __name__)

COURSE_CATEGORIES = {
    'web-mobile': {
        'name': 'Web & Mobile Development',
        'courses': [
            {
                'title': 'Frontend Web Development',
                'description': 'Learn HTML5, CSS3, JavaScript, and modern frameworks',
                'levels': ['Beginner', 'Intermediate', 'Advanced'],
                'topics': ['HTML/CSS Fundamentals', 'JavaScript ES6+', 'React/Vue.js', 'Responsive Design'],
                'resources': {
                    'tutorials': ['MDN Web Docs', 'freeCodeCamp', 'Traversy Media'],
                    'tools': ['VS Code', 'Chrome DevTools', 'Git'],
                    'community': ['Stack Overflow', 'Dev.to', 'Frontend Masters']
                }
            },
            {
                'title': 'Mobile App Development',
                'description': 'Build cross-platform mobile applications',
                'levels': ['Intermediate', 'Advanced'],
                'topics': ['React Native', 'Flutter', 'Native APIs', 'App Publishing'],
                'resources': {
                    'tutorials': ['React Native Docs', 'Flutter Dev', 'Academind'],
                    'tools': ['Android Studio', 'Xcode', 'Expo'],
                    'community': ['React Native Community', 'Flutter Dev Community']
                }
            }
        ]
    },
    'animation': {
        'name': 'Animation & Motion Graphics',
        'courses': [
            {
                'title': '2D Animation Fundamentals',
                'description': 'Master the principles of 2D animation',
                'levels': ['Beginner', 'Intermediate'],
                'topics': ['Animation Principles', 'Character Animation', 'Motion Graphics'],
                'resources': {
                    'tutorials': ['School of Motion', 'Animation Mentor', 'Bloop Animation'],
                    'tools': ['Adobe Animate', 'ToonBoom Harmony', 'After Effects'],
                    'community': ['Animation World Network', 'CartoonBrew']
                }
            }
        ]
    },
    'networking': {
        'name': 'Networking',
        'courses': [
            {
                'title': 'Network Administration',
                'description': 'Learn network infrastructure and management',
                'levels': ['Beginner', 'Intermediate', 'Advanced'],
                'topics': ['TCP/IP', 'Network Security', 'Cloud Infrastructure'],
                'resources': {
                    'tutorials': ['Cisco Learning', 'CompTIA', 'NetworkChuck'],
                    'tools': ['Wireshark', 'Cisco Packet Tracer', 'GNS3'],
                    'community': ['TechExams.net', 'r/networking']
                }
            }
        ]
    },
    'graphics': {
        'name': 'Graphics & Visualization',
        'courses': [
            {
                'title': '3D Graphics Programming',
                'description': 'Create stunning 3D graphics applications',
                'levels': ['Intermediate', 'Advanced'],
                'topics': ['OpenGL', 'WebGL', 'Three.js', 'Shader Programming'],
                'resources': {
                    'tutorials': ['LearnOpenGL', 'ThreeJS Fundamentals', 'Shadertoy'],
                    'tools': ['Blender', 'Unity', 'Visual Studio'],
                    'community': ['Graphics Programming Discord', 'OpenGL Forum']
                }
            }
        ]
    },
    'game-dev': {
        'name': 'Game Animation',
        'courses': [
            {
                'title': 'Game Animation Development',
                'description': 'Create engaging game animations',
                'levels': ['Intermediate', 'Advanced'],
                'topics': ['Character Rigging', 'Animation States', 'Unity Animation'],
                'resources': {
                    'tutorials': ['Unity Learn', 'Unreal Engine Docs', 'GDC Vault'],
                    'tools': ['Unity', 'Unreal Engine', 'Maya'],
                    'community': ['Unity Forums', 'Unreal Engine Community']
                }
            }
        ]
    },
    'info-security': {
        'name': 'Information Security',
        'courses': [
            {
                'title': 'Cybersecurity Fundamentals',
                'description': 'Learn essential security concepts and practices',
                'levels': ['Beginner', 'Intermediate', 'Advanced'],
                'topics': ['Security Fundamentals', 'Ethical Hacking', 'Security Auditing'],
                'resources': {
                    'tutorials': ['Cybrary', 'HackTheBox', 'SANS Institute'],
                    'tools': ['Kali Linux', 'Metasploit', 'Wireshark'],
                    'community': ['HackTheBox Forums', 'r/netsec']
                }
            }
        ]
    }
}

@bp.route('/courses')
def index():
    return render_template('courses/index.html', categories=COURSE_CATEGORIES)

@bp.route('/courses/<category>')
def category(category):
    if category not in COURSE_CATEGORIES:
        flash('Category not found', 'error')
        return redirect(url_for('courses.index'))
    return render_template('courses/category.html', category=COURSE_CATEGORIES[category])

@bp.route('/courses/<category>/<course_id>')
def course(category, course_id):
    if category not in COURSE_CATEGORIES:
        flash('Category not found', 'error')
        return redirect(url_for('courses.index'))
    
    courses = COURSE_CATEGORIES[category]['courses']
    try:
        course = courses[int(course_id)]
    except (ValueError, IndexError):
        flash('Course not found', 'error')
        return redirect(url_for('courses.category', category=category))
    
    return render_template('courses/course.html', course=course)

@bp.route('/course/<int:course_id>/upload', methods=['POST'])
@login_required
def upload_content(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Check if user is the course instructor
    if current_user.id != course.instructor_id:
        flash('You do not have permission to upload content to this course.', 'error')
        return redirect(url_for('courses.view', course_id=course_id))
    
    if 'file' not in request.files:
        flash('No file uploaded.', 'error')
        return redirect(url_for('courses.view', course_id=course_id))
        
    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('courses.view', course_id=course_id))
    
    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        # Initialize Drive service
        token_info = {
            'access_token': current_user.google_token,
            'refresh_token': current_user.google_refresh_token,
        }
        drive_service.initialize_service(token_info)
        
        # Create course folders if they don't exist
        if not course.video_folder_id or not course.material_folder_id:
            folders = drive_service.create_course_folders(course.title)
            course.video_folder_id = folders['video_folder_id']
            course.material_folder_id = folders['material_folder_id']
            db.session.commit()
        
        # Upload to appropriate folder based on content type
        content_type = request.form.get('content_type')
        folder_id = course.video_folder_id if content_type == 'video' else course.material_folder_id
        
        # Upload to Drive
        result = drive_service.upload_content(temp_path, folder_id, content_type)
        
        # Create CourseContent record
        content = CourseContent(
            title=request.form.get('title'),
            description=request.form.get('description'),
            course_id=course_id,
            content_type=content_type,
            drive_file_id=result['file_id'],
            drive_view_link=result['view_link'],
            order=len(course.contents) + 1
        )
        db.session.add(content)
        db.session.commit()
        
        # Clean up temporary file
        os.remove(temp_path)
        
        flash('Content uploaded successfully!', 'success')
        
    except Exception as e:
        current_app.logger.error(f"Error uploading content: {str(e)}")
        flash('Error uploading content. Please try again.', 'error')
        
    return redirect(url_for('courses.view', course_id=course_id))

@bp.route('/course/<int:course_id>/content/<int:content_id>/delete', methods=['POST'])
@login_required
def delete_content(course_id, content_id):
    course = Course.query.get_or_404(course_id)
    content = CourseContent.query.get_or_404(content_id)
    
    # Check if user is the course instructor
    if current_user.id != course.instructor_id:
        flash('You do not have permission to delete content from this course.', 'error')
        return redirect(url_for('courses.view', course_id=course_id))
    
    try:
        # Initialize Drive service
        token_info = {
            'access_token': current_user.google_token,
            'refresh_token': current_user.google_refresh_token,
        }
        drive_service.initialize_service(token_info)
        
        # Delete from Drive
        if content.drive_file_id:
            drive_service.delete_file(content.drive_file_id)
        
        # Delete from database
        db.session.delete(content)
        db.session.commit()
        
        flash('Content deleted successfully!', 'success')
        
    except Exception as e:
        current_app.logger.error(f"Error deleting content: {str(e)}")
        flash('Error deleting content. Please try again.', 'error')
    
    return redirect(url_for('courses.view', course_id=course_id))