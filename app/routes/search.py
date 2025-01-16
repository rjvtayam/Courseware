from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from elasticsearch_dsl import Search
from app import elasticsearch
from app.models import Course, Assignment, User

bp = Blueprint('search', __name__)

@bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    filters = {
        'type': request.args.get('type', 'all'),  # courses, assignments, users
        'status': request.args.get('status'),      # active, archived
        'date_from': request.args.get('date_from'),
        'date_to': request.args.get('date_to'),
        'sort_by': request.args.get('sort_by', 'relevance')  # relevance, date, title
    }
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Base search query
    s = Search(using=elasticsearch)
    
    # Apply type filter
    if filters['type'] != 'all':
        s = s.filter('term', type=filters['type'])
    
    # Apply status filter
    if filters['status']:
        s = s.filter('term', status=filters['status'])
    
    # Apply date range filter
    if filters['date_from'] or filters['date_to']:
        date_filter = {}
        if filters['date_from']:
            date_filter['gte'] = filters['date_from']
        if filters['date_to']:
            date_filter['lte'] = filters['date_to']
        s = s.filter('range', created_at=date_filter)
    
    # Apply sorting
    if filters['sort_by'] == 'date':
        s = s.sort('-created_at')
    elif filters['sort_by'] == 'title':
        s = s.sort('title.keyword')
    
    # Add query
    if query:
        s = s.query('multi_match', 
                   query=query,
                   fields=['title^3', 'description^2', 'content'])
    
    # Pagination
    s = s[(page-1)*per_page:page*per_page]
    
    # Execute search
    response = s.execute()
    
    return render_template('search/results.html',
                         results=response,
                         query=query,
                         filters=filters,
                         page=page,
                         total=response.hits.total.value)

@bp.route('/api/search-suggestions')
@login_required
def search_suggestions():
    """API endpoint for search autocomplete"""
    query = request.args.get('q', '')
    
    s = Search(using=elasticsearch)\
        .query('multi_match',
              query=query,
              fields=['title^3', 'description^2'])\
        .source(['title', 'type'])\
        [:5]
    
    response = s.execute()
    
    suggestions = [{'title': hit.title, 'type': hit.type} 
                  for hit in response]
    
    return jsonify(suggestions)