from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from functools import wraps
from flask import session, redirect, url_for, flash
import os


ph = PasswordHasher()


def hash_password(password):
    """Hash a password using argon2"""
    return ph.hash(password)


def verify_password(password_hash, password):
    """Verify a password against its hash"""
    try:
        ph.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False


def login_user(username, password):
    """Validate login credentials"""
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password_hash = os.getenv('ADMIN_PASSWORD_HASH', '')
    
    if not admin_password_hash:
        return False, "Admin password not configured"
    
    if username != admin_username:
        return False, "Invalid username or password"
    
    if not verify_password(admin_password_hash, password):
        return False, "Invalid username or password"
    
    session['logged_in'] = True
    session['username'] = username
    session.permanent = True
    
    return True, "Login successful"


def logout_user():
    """Clear user session"""
    session.clear()


def is_logged_in():
    """Check if user is logged in"""
    return session.get('logged_in', False)


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please login to access this page', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
