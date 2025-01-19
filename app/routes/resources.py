from flask import Blueprint, render_template, flash, redirect, url_for

bp = Blueprint('resources', __name__, url_prefix='/resources')

# Documentation Resources
def get_documentation_resources():
    return {
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

# Development Tools
def get_tools_resources():
    return {
        'bsit': {
            'name': 'BSIT Development Tools',
            'resources': [
                {
                    'name': 'Visual Studio Code',
                    'url': 'https://code.visualstudio.com/',
                    'description': 'Lightweight but powerful source code editor.',
                    'tags': ['Editor', 'BSIT']
                },
                {
                    'name': 'XAMPP',
                    'url': 'https://www.apachefriends.org/',
                    'description': 'Web development environment with Apache, MySQL, and PHP.',
                    'tags': ['Web Development', 'BSIT']
                }
            ]
        },
        'bscs': {
            'name': 'BSCS Development Tools',
            'resources': [
                {
                    'name': 'Visual Studio',
                    'url': 'https://visualstudio.microsoft.com/',
                    'description': 'Full-featured IDE for C++, C#, and more.',
                    'tags': ['IDE', 'BSCS']
                },
                {
                    'name': 'Unity Hub',
                    'url': 'https://unity.com/download',
                    'description': 'Game development platform and editor.',
                    'tags': ['Game Development', 'BSCS']
                }
            ]
        },
        'bsis': {
            'name': 'BSIS Development Tools',
            'resources': [
                {
                    'name': 'Jupyter Notebook',
                    'url': 'https://jupyter.org/',
                    'description': 'Interactive computing environment for data science.',
                    'tags': ['Data Science', 'BSIS']
                },
                {
                    'name': 'Wireshark',
                    'url': 'https://www.wireshark.org/',
                    'description': 'Network protocol analyzer for security analysis.',
                    'tags': ['Security', 'BSIS']
                }
            ]
        }
    }

# Online Platforms
def get_online_platforms():
    return {
        'bsit': {
            'name': 'BSIT Online Learning Platforms',
            'resources': [
                {
                    'name': 'freeCodeCamp',
                    'url': 'https://www.freecodecamp.org/',
                    'description': 'Learn web development with free interactive tutorials.',
                    'tags': ['Web Development', 'BSIT']
                },
                {
                    'name': 'Cisco Networking Academy',
                    'url': 'https://www.netacad.com/',
                    'description': 'Learn networking concepts and get certified.',
                    'tags': ['Networking', 'BSIT']
                }
            ]
        },
        'bscs': {
            'name': 'BSCS Online Learning Platforms',
            'resources': [
                {
                    'name': 'Coursera',
                    'url': 'https://www.coursera.org/',
                    'description': 'Online courses from top universities.',
                    'tags': ['Programming', 'BSCS']
                },
                {
                    'name': 'Unity Learn',
                    'url': 'https://learn.unity.com/',
                    'description': 'Official Unity tutorials and courses.',
                    'tags': ['Game Development', 'BSCS']
                }
            ]
        },
        'bsis': {
            'name': 'BSIS Online Learning Platforms',
            'resources': [
                {
                    'name': 'DataCamp',
                    'url': 'https://www.datacamp.com/',
                    'description': 'Interactive data science courses.',
                    'tags': ['Data Science', 'BSIS']
                },
                {
                    'name': 'TryHackMe',
                    'url': 'https://tryhackme.com/',
                    'description': 'Learn cybersecurity through hands-on exercises.',
                    'tags': ['Security', 'BSIS']
                }
            ]
        }
    }

# Routes
@bp.route('/documentation')
def documentation():
    return render_template('resources/documentation.html', docs=get_documentation_resources())

@bp.route('/tools')
def tools():
    return render_template('resources/tools.html', tools=get_tools_resources())

@bp.route('/online-platforms')
def online_platforms():
    return render_template('resources/online_platforms.html', platforms=get_online_platforms())

RESOURCE_CATEGORIES = {
    'platforms': {
        'name': 'Online Learning Platforms',
        'resources': [
            {
                'name': 'Coursera',
                'url': 'https://www.coursera.org',
                'description': 'Online courses from top universities',
                'categories': ['web-mobile', 'graphics', 'info-security']
            },
            {
                'name': 'Udemy',
                'url': 'https://www.udemy.com',
                'description': 'Comprehensive courses on various topics',
                'categories': ['web-mobile', 'animation', 'game-dev']
            },
            {
                'name': 'LinkedIn Learning',
                'url': 'https://www.linkedin.com/learning',
                'description': 'Professional development courses',
                'categories': ['service-management', 'networking']
            }
        ]
    },
    'documentation': {
        'name': 'Technical Documentation',
        'resources': [
            {
                'name': 'MDN Web Docs',
                'url': 'https://developer.mozilla.org',
                'description': 'Comprehensive web development documentation',
                'categories': ['web-mobile']
            },
            {
                'name': 'Unity Documentation',
                'url': 'https://docs.unity3d.com',
                'description': 'Official Unity engine documentation',
                'categories': ['game-dev', 'graphics']
            }
        ]
    },
    'development-tools': {
        'name': 'Development Tools',
        'resources': [
            {
                'name': 'Visual Studio Code',
                'url': 'https://code.visualstudio.com',
                'description': 'Popular code editor with extensive plugin support',
                'categories': ['web-mobile', 'game-dev']
            },
            {
                'name': 'GitHub',
                'url': 'https://github.com',
                'description': 'Version control and collaboration platform',
                'categories': ['web-mobile', 'game-dev', 'graphics']
            },
            {
                'name': 'Figma',
                'url': 'https://www.figma.com',
                'description': 'Collaborative interface design tool',
                'categories': ['web-mobile', 'animation']
            }
        ]
    },
    'design-tools': {
        'name': 'Design Software',
        'resources': [
            {
                'name': 'Adobe Creative Cloud',
                'url': 'https://www.adobe.com/creativecloud.html',
                'description': 'Suite of professional design tools',
                'categories': ['animation', 'graphics']
            },
            {
                'name': 'Blender',
                'url': 'https://www.blender.org',
                'description': 'Free and open-source 3D creation suite',
                'categories': ['animation', 'game-dev', 'graphics']
            }
        ]
    },
    'youtube': {
        'name': 'Educational YouTube Channels',
        'resources': [
            {
                'name': 'Traversy Media',
                'url': 'https://www.youtube.com/user/TechGuyWeb',
                'description': 'Web development tutorials',
                'categories': ['web-mobile']
            },
            {
                'name': 'The Coding Train',
                'url': 'https://www.youtube.com/user/shiffman',
                'description': 'Creative coding tutorials',
                'categories': ['graphics', 'game-dev']
            },
            {
                'name': 'NetworkChuck',
                'url': 'https://www.youtube.com/c/NetworkChuck',
                'description': 'Networking and cybersecurity tutorials',
                'categories': ['networking', 'info-security']
            }
        ]
    },
    'forums': {
        'name': 'Forums & Communities',
        'resources': [
            {
                'name': 'Stack Overflow',
                'url': 'https://stackoverflow.com',
                'description': 'Q&A community for programmers',
                'categories': ['web-mobile', 'graphics', 'game-dev']
            },
            {
                'name': 'Reddit r/learnprogramming',
                'url': 'https://www.reddit.com/r/learnprogramming/',
                'description': 'Programming learning community',
                'categories': ['web-mobile', 'game-dev']
            },
            {
                'name': 'Unity Forums',
                'url': 'https://forum.unity.com',
                'description': 'Official Unity community forums',
                'categories': ['game-dev', 'graphics']
            }
        ]
    }
}

@bp.route('/')
def index():
    return render_template('resources/index.html', categories=RESOURCE_CATEGORIES)

@bp.route('/<category>')
def category(category):
    if category not in RESOURCE_CATEGORIES:
        flash('Category not found', 'error')
        return redirect(url_for('resources.index'))
    return render_template('resources/category.html', category=RESOURCE_CATEGORIES[category])
