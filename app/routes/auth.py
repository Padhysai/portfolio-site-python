from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.services import auth_manager
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            return redirect(request.args.get('next') or url_for('admin.dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/login/google')
def google_login():
    redirect_uri = url_for('auth.google_callback', _external=True)
    return auth_manager.oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/callback')
def google_callback():
    try:
        token = auth_manager.oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        if user_info and user_info.get('email') == current_app.config['ADMIN_EMAIL']:
            session['logged_in'] = True
            session['user_email'] = user_info.get('email')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Unauthorized Google Account. Please use the Admin email.')
            return redirect(url_for('auth.login'))
    except Exception as e:
        flash(f'Google Login Failed: {str(e)}')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
