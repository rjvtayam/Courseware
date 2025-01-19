from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
from app.models.models import User
from app import db

bp = Blueprint('auth', __name__)

# OAuth 2.0 client setup
google_client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])
github_client = WebApplicationClient(current_app.config['GITHUB_CLIENT_ID'])

def get_google_provider_cfg():
    return requests.get(current_app.config['GOOGLE_DISCOVERY_URL']).json()

@bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('workspace.dashboard'))  # Redirect to workspace dashboard
    return render_template('auth/login.html')

@bp.route('/login/google')
def google_login():
    # Get role from query parameters
    role = request.args.get('role', 'student')
    session['user_role'] = role  # Store role in session
    
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for('auth.google_callback', _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@bp.route('/login/github')
def github_login():
    # Get role from query parameters
    role = request.args.get('role', 'student')
    session['user_role'] = role  # Store role in session
    
    # GitHub's OAuth flow
    github_auth_url = f"https://github.com/login/oauth/authorize"
    request_uri = github_client.prepare_request_uri(
        github_auth_url,
        redirect_uri=url_for('auth.github_callback', _external=True),
        scope=['user:email']
    )
    return redirect(request_uri)

@bp.route('/login/google/callback')
def google_callback():
    # Get authorization code Google sent back
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens
    token_url, headers, body = google_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=url_for('auth.google_callback', _external=True),
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config['GOOGLE_CLIENT_ID'], current_app.config['GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens
    google_client.parse_request_body_response(json.dumps(token_response.json()))

    # Get user info from Google
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = google_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        
        # Get role from session
        is_teacher = session.pop('user_role', 'student') == 'teacher'
    else:
        flash("User email not available or not verified by Google.", "error")
        return redirect(url_for("auth.login"))

    # Create a user in our db with the information provided by Google
    user = User.query.filter_by(email=users_email).first()
    if not user:
        user = User(
            username=users_name,
            email=users_email,
            google_id=unique_id,
            oauth_provider='google',
            is_teacher=is_teacher
        )
        db.session.add(user)
        db.session.commit()
        flash("Welcome! Your account has been created successfully.", "success")

    # Begin user session by logging the user in
    login_user(user)
    return redirect(url_for('workspace.dashboard'))  # Redirect to workspace dashboard

@bp.route('/login/github/callback')
def github_callback():
    # Get the authorization code
    code = request.args.get("code")
    
    # Prepare request to get access token
    token_url = "https://github.com/login/oauth/access_token"
    token_params = {
        'client_id': current_app.config['GITHUB_CLIENT_ID'],
        'client_secret': current_app.config['GITHUB_CLIENT_SECRET'],
        'code': code,
    }
    
    # Get access token
    token_response = requests.post(token_url, data=token_params, headers={'Accept': 'application/json'})
    access_token = token_response.json().get('access_token')
    
    # Get user info from GitHub
    github_user_url = "https://api.github.com/user"
    github_email_url = "https://api.github.com/user/emails"
    headers = {'Authorization': f'token {access_token}'}
    
    github_user = requests.get(github_user_url, headers=headers).json()
    github_emails = requests.get(github_email_url, headers=headers).json()
    
    # Get primary email
    github_email = next(
        (email['email'] for email in github_emails if email['primary']),
        github_emails[0]['email'] if github_emails else None
    )
    
    if not github_email:
        flash("Could not get email from GitHub.", "error")
        return redirect(url_for("auth.login"))
    
    # Get role from session
    is_teacher = session.pop('user_role', 'student') == 'teacher'
    
    # Create/update user in database
    user = User.query.filter_by(email=github_email).first()
    if not user:
        user = User(
            username=github_user['login'],
            email=github_email,
            github_id=str(github_user['id']),
            oauth_provider='github',
            is_teacher=is_teacher
        )
        db.session.add(user)
        db.session.commit()
        flash("Welcome! Your account has been created successfully.", "success")

    login_user(user)
    return redirect(url_for('workspace.dashboard'))  # Redirect to workspace dashboard

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('main.index'))