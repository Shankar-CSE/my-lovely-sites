from flask import Flask, jsonify
from app.config import Config
from app.db import close_db, test_connection
import atexit


def create_app(config_class=Config):
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Health check endpoint
    @app.route('/health')
    def health():
        """Health check endpoint for deployment platforms"""
        db_status = 'connected' if test_connection() else 'disconnected'
        return jsonify({
            'status': 'ok',
            'database': db_status
        }), 200 if db_status == 'connected' else 503
    
    # Register routes
    from app.routes import public, admin, auth
    app.register_blueprint(public.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    
    # Close DB connection on shutdown
    atexit.register(close_db)
    
    return app
