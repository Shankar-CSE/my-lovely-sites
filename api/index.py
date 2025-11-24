import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import create_app
    
    # Create the Flask app instance for Vercel with production config
    app = create_app('production')
    
    # Vercel needs the app object to be named 'app'
    # This is the WSGI application that Vercel will call
    
except Exception as e:
    # If there's an error during startup, create a minimal app to show it
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({
            'error': 'Application failed to start',
            'message': str(e),
            'type': type(e).__name__
        }), 500
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'error', 'message': str(e)}), 503
