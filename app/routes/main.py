from flask import Blueprint, render_template
from flask_login import current_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('welcome/welcome.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/privacy')
def privacy():
    return render_template('legal/privacy.html')

@bp.route('/terms')
def terms():
    return render_template('legal/terms.html')

@bp.route('/resources/online-platforms')
def online_platforms():
    platforms = {
        'bsit': {
            'name': 'BSIT Online Learning Platforms',
            'resources': [
                {
                    'name': 'Coursera - Web Development Specialization',
                    'url': 'https://www.coursera.org/specializations/web-development',
                    'description': 'Comprehensive web development courses covering HTML, CSS, JavaScript, and modern frameworks.',
                    'tags': ['Web Development', 'BSIT']
                },
                {
                    'name': 'Udacity - Cloud Computing',
                    'url': 'https://www.udacity.com/course/cloud-computing',
                    'description': 'Learn cloud architecture and deployment with hands-on projects.',
                    'tags': ['Networking', 'Cloud']
                },
                {
                    'name': 'LinkedIn Learning - Motion Graphics',
                    'url': 'https://www.linkedin.com/learning/topics/motion-graphics',
                    'description': 'Professional motion graphics and animation tutorials.',
                    'tags': ['Animation', 'Graphics']
                }
            ]
        },
        'bscs': {
            'name': 'BSCS Online Learning Platforms',
            'resources': [
                {
                    'name': 'Unity Learn',
                    'url': 'https://learn.unity.com/',
                    'description': 'Official Unity game development tutorials and courses.',
                    'tags': ['Game Development', 'BSCS']
                },
                {
                    'name': 'OpenGL Tutorial',
                    'url': 'https://learnopengl.com/',
                    'description': 'Comprehensive OpenGL tutorials for graphics programming.',
                    'tags': ['Graphics', 'Visualization']
                }
            ]
        },
        'bsis': {
            'name': 'BSIS Online Learning Platforms',
            'resources': [
                {
                    'name': 'Cybrary',
                    'url': 'https://www.cybrary.it/',
                    'description': 'Cybersecurity and IT security training platform.',
                    'tags': ['Security', 'BSIS']
                },
                {
                    'name': 'DataCamp',
                    'url': 'https://www.datacamp.com/',
                    'description': 'Interactive data science and analytics courses.',
                    'tags': ['Data Analytics', 'BSIS']
                }
            ]
        }
    }
    return render_template('resources/online_platforms.html', platforms=platforms)

@bp.route('/resources/documentation')
def documentation():
    docs = {
        'bsit': {
            'name': 'BSIT Documentation Resources',
            'resources': [
                {
                    'name': 'MDN Web Docs',
                    'url': 'https://developer.mozilla.org/',
                    'description': 'Comprehensive documentation for web technologies.',
                    'tags': ['Web Development', 'BSIT']
                },
                {
                    'name': 'Cisco Documentation',
                    'url': 'https://www.cisco.com/c/en/us/support/index.html',
                    'description': 'Official Cisco networking documentation.',
                    'tags': ['Networking', 'BSIT']
                }
            ]
        },
        'bscs': {
            'name': 'BSCS Documentation Resources',
            'resources': [
                {
                    'name': 'OpenGL Documentation',
                    'url': 'https://www.opengl.org/documentation/',
                    'description': 'Official OpenGL documentation and specifications.',
                    'tags': ['Graphics', 'BSCS']
                },
                {
                    'name': 'Unreal Engine Docs',
                    'url': 'https://docs.unrealengine.com/',
                    'description': 'Official Unreal Engine documentation for game development.',
                    'tags': ['Game Development', 'BSCS']
                }
            ]
        },
        'bsis': {
            'name': 'BSIS Documentation Resources',
            'resources': [
                {
                    'name': 'OWASP Documentation',
                    'url': 'https://owasp.org/www-project-web-security-testing-guide/',
                    'description': 'Web security testing guide and best practices.',
                    'tags': ['Security', 'BSIS']
                },
                {
                    'name': 'Python Data Science Handbook',
                    'url': 'https://jakevdp.github.io/PythonDataScienceHandbook/',
                    'description': 'Comprehensive guide for data science with Python.',
                    'tags': ['Data Analytics', 'BSIS']
                }
            ]
        }
    }
    return render_template('resources/documentation.html', docs=docs)

@bp.route('/resources/tools')
def tools():
    tools = {
        'bsit': {
            'name': 'BSIT Development Tools',
            'resources': [
                {
                    'name': 'Visual Studio Code',
                    'url': 'https://code.visualstudio.com/',
                    'description': 'Popular code editor with extensive web development support.',
                    'tags': ['Web Development', 'BSIT']
                },
                {
                    'name': 'Adobe Creative Cloud',
                    'url': 'https://www.adobe.com/creativecloud.html',
                    'description': 'Professional tools for animation and graphics.',
                    'tags': ['Animation', 'Graphics']
                },
                {
                    'name': 'Wireshark',
                    'url': 'https://www.wireshark.org/',
                    'description': 'Network protocol analyzer for networking professionals.',
                    'tags': ['Networking', 'BSIT']
                }
            ]
        },
        'bscs': {
            'name': 'BSCS Development Tools',
            'resources': [
                {
                    'name': 'Unity',
                    'url': 'https://unity.com/',
                    'description': 'Leading game development platform.',
                    'tags': ['Game Development', 'BSCS']
                },
                {
                    'name': 'Blender',
                    'url': 'https://www.blender.org/',
                    'description': '3D creation suite for modeling and animation.',
                    'tags': ['Graphics', 'BSCS']
                }
            ]
        },
        'bsis': {
            'name': 'BSIS Tools',
            'resources': [
                {
                    'name': 'Metasploit',
                    'url': 'https://www.metasploit.com/',
                    'description': 'Penetration testing framework.',
                    'tags': ['Security', 'BSIS']
                },
                {
                    'name': 'Tableau',
                    'url': 'https://www.tableau.com/',
                    'description': 'Data visualization and analytics platform.',
                    'tags': ['Data Analytics', 'BSIS']
                }
            ]
        }
    }
    return render_template('resources/tools.html', tools=tools)
