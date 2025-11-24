import sys
import os
import traceback

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask first for fallback error handling
from flask import Flask, jsonify, request

# Try to create the actual app
try:
    from app import create_app
    
    # Create the Flask app instance for Vercel with production config
    app = create_app('production')
    
    print("✓ Application started successfully")
    
except Exception as e:
    # If there's an error during startup, create a minimal app to show it
    print(f"✗ Application startup failed: {str(e)}")
    print(f"Traceback: {traceback.format_exc()}")
    
    app = Flask(__name__)
    
    startup_error = {
        'error': 'Application failed to start',
        'message': str(e),
        'type': type(e).__name__,
        'traceback': traceback.format_exc()
    }
    
    @app.route('/')
    def error():
        return jsonify(startup_error), 500
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'error', 'message': str(e)}), 503
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }), 500

# Add a catch-all error handler to show detailed errors
@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({
        'error': str(e),
        'type': type(e).__name__,
        'path': request.path,
        'method': request.method,
        'traceback': traceback.format_exc()
    }), 500

# Add debug endpoint to check environment
@app.route('/debug')
def debug():
    """Debug endpoint to check configuration"""
    import os
    return jsonify({
        'environment_variables': {
            'MONGO_URI': 'SET' if os.getenv('MONGO_URI') else 'NOT SET',
            'SECRET_KEY': 'SET' if os.getenv('SECRET_KEY') else 'NOT SET',
            'ADMIN_USERNAME': 'SET' if os.getenv('ADMIN_USERNAME') else 'NOT SET',
            'ADMIN_PASSWORD_HASH': 'SET' if os.getenv('ADMIN_PASSWORD_HASH') else 'NOT SET',
            'FLASK_ENV': os.getenv('FLASK_ENV', 'NOT SET'),
        },
        'python_version': sys.version,
        'working_directory': os.getcwd(),
        'app_name': app.name if app else 'No app',
    })
