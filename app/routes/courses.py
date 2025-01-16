from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.models import Course, User
from app import db

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