from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import login_user, logout_user, is_logged_in

bp = Blueprint('auth', __name__, url_prefix='/admin')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    # Redirect if already logged in
    if is_logged_in():
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'error')
        else:
            success, message = login_user(username, password)
            
            if success:
                flash(message, 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash(message, 'error')
    
    return render_template('login.html')


@bp.route('/logout', methods=['POST'])
def logout():
    """Logout"""
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('public.index'))
