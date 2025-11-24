import os
from app import create_app

env = os.getenv('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # Only use debug and auto-reload in development
    is_dev = env == 'development'
    app.run(
        debug=is_dev,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )
