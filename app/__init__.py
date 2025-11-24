from flask import Flask, jsonify
from app.config import config
from app.db import close_db, test_connection
import atexit


def create_app(config_name='default'):
    """Flask application factory"""
    app = Flask(__name__)
    
    # Load configuration based on environment
    app.config.from_object(config[config_name])
    
    # Add security headers to all responses
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses"""
        security_headers = app.config.get('SECURITY_HEADERS', {})
        for header, value in security_headers.items():
            response.headers[header] = value
        return response
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors"""
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 errors"""
        return jsonify({'error': 'Internal server error'}), 500
    
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
