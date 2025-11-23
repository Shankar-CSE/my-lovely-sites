from flask import Flask
from app.config import Config
from app.db import get_db, close_db
import atexit


def create_app(config_class=Config):
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database connection
    with app.app_context():
        get_db()
    
    # Register routes
    from app.routes import public, admin, auth
    app.register_blueprint(public.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    
    # Close DB connection on shutdown
    atexit.register(close_db)
    
    return app
