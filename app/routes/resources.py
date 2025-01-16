from flask import Blueprint, render_template, flash, redirect, url_for

bp = Blueprint('resources', __name__)

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

@bp.route('/resources')
def index():
    return render_template('resources/index.html', categories=RESOURCE_CATEGORIES)

@bp.route('/resources/<category>')
def category(category):
    if category not in RESOURCE_CATEGORIES:
        flash('Category not found', 'error')
        return redirect(url_for('resources.index'))
    return render_template('resources/category.html', category=RESOURCE_CATEGORIES[category])
