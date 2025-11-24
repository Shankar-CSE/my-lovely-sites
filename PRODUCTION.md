# Production Deployment Guide

This guide will help you deploy the URL Organizer application to production.

## Pre-Deployment Checklist

### 1. Environment Configuration

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Update the following values:

```env
# Generate a strong secret key
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Use MongoDB Atlas for production
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/url_organizer?retryWrites=true&w=majority

# Set admin credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=your_hashed_password

# Set environment to production
FLASK_ENV=production

# Optional: Custom port
PORT=5000
```

### 2. Generate Admin Password Hash

```bash
python scripts/hash_password.py
```

Copy the generated hash to your `.env` file as `ADMIN_PASSWORD_HASH`.

### 3. Database Setup

Run the index fix script to ensure proper MongoDB indexes:

```bash
python scripts/fix_url_index.py
```

### 4. Test the Application Locally

```bash
FLASK_ENV=production python run.py
```

Visit `http://localhost:5000` and verify:
- ✅ All pages load correctly
- ✅ Dark mode toggle works
- ✅ Login functionality works
- ✅ CRUD operations work
- ✅ Search and filtering work

## Deployment Options

### Option 1: Vercel (Recommended for Quick Deploy)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables in Vercel dashboard:
   - `SECRET_KEY`
   - `MONGO_URI`
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD_HASH`
   - `FLASK_ENV=production`

The `vercel.json` configuration is already set up.

### Option 2: Traditional Server (VPS/Cloud)

#### Using Gunicorn (Recommended)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

For production, use systemd service:

Create `/etc/systemd/system/url-organizer.service`:

```ini
[Unit]
Description=URL Organizer Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/url-organizer
Environment="PATH=/path/to/venv/bin"
Environment="FLASK_ENV=production"
EnvironmentFile=/path/to/url-organizer/.env
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable url-organizer
sudo systemctl start url-organizer
```

#### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/url-organizer`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/url-organizer/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/url-organizer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 3: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - MONGO_URI=${MONGO_URI}
      - SECRET_KEY=${SECRET_KEY}
      - ADMIN_USERNAME=${ADMIN_USERNAME}
      - ADMIN_PASSWORD_HASH=${ADMIN_PASSWORD_HASH}
    restart: unless-stopped

  mongodb:
    image: mongo:7
    volumes:
      - mongo_data:/data/db
    restart: unless-stopped

volumes:
  mongo_data:
```

Deploy:
```bash
docker-compose up -d
```

### Option 4: Platform-as-a-Service

#### Render.com

1. Connect your GitHub repository
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn -w 4 -b 0.0.0.0:$PORT run:app`
5. Add environment variables in dashboard

#### Railway.app

1. Connect your GitHub repository
2. Add MongoDB plugin
3. Set environment variables
4. Deploy automatically

#### Heroku

1. Create `Procfile`:
```
web: gunicorn run:app
```

2. Deploy:
```bash
heroku create your-app-name
heroku addons:create mongolab:sandbox
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set ADMIN_USERNAME="admin"
heroku config:set ADMIN_PASSWORD_HASH="your-hash"
heroku config:set FLASK_ENV="production"
git push heroku main
```

## Security Checklist

- ✅ Strong `SECRET_KEY` (32+ random bytes)
- ✅ Secure MongoDB connection (MongoDB Atlas with IP whitelist)
- ✅ Strong admin password (hashed with Argon2)
- ✅ HTTPS enabled (SSL certificate)
- ✅ Security headers enabled (HSTS, X-Frame-Options, etc.)
- ✅ Session cookies are secure and httponly
- ✅ `.env` file not committed to git (in `.gitignore`)
- ✅ Debug mode disabled in production
- ✅ Error pages don't expose sensitive information

## Performance Optimization

### MongoDB Indexes

The application automatically creates indexes on:
- `url` (unique, sparse)
- `tags`
- `created_at`
- Text search on `title` and `description`

### Caching

For high-traffic sites, consider adding Redis for caching:

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL')
})

@cache.cached(timeout=300)
def expensive_operation():
    # Your code here
    pass
```

### CDN for Static Assets

For production, serve static assets via CDN:
- Upload assets to S3/CloudFront or similar
- Update template references

## Monitoring

### Health Check Endpoint

The application includes a `/health` endpoint for monitoring:

```bash
curl https://your-domain.com/health
```

Response:
```json
{
  "status": "ok",
  "database": "connected"
}
```

### Logging

Configure logging in production:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Error Tracking

Consider integrating Sentry for error tracking:

```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

## Backup Strategy

### MongoDB Backups

#### Automated Backups (MongoDB Atlas)
- Enable continuous backups in Atlas dashboard
- Set retention policy (7-35 days)

#### Manual Backups
```bash
mongodump --uri="your-mongo-uri" --out=/backup/$(date +%Y%m%d)
```

#### Automated Backup Script
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mongodump --uri="$MONGO_URI" --out="/backups/$DATE"
# Upload to S3 or similar
aws s3 sync "/backups/$DATE" "s3://your-bucket/backups/$DATE"
```

## Maintenance

### Updating Dependencies

```bash
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
```

### Database Migrations

When schema changes:
1. Test on staging environment
2. Backup database
3. Run migration scripts
4. Verify data integrity

### Rolling Updates

For zero-downtime deployments:
1. Use blue-green deployment
2. Or rolling updates with load balancer
3. Test health endpoint before routing traffic

## Troubleshooting

### Application Won't Start

Check:
- Environment variables are set correctly
- MongoDB is accessible
- Port is not already in use
- Logs for specific errors

### Database Connection Issues

- Verify `MONGO_URI` is correct
- Check network connectivity
- Verify MongoDB Atlas IP whitelist
- Check credentials

### Performance Issues

- Monitor MongoDB query performance
- Check server resources (CPU, RAM)
- Review application logs
- Consider scaling horizontally

## Support

For issues or questions:
- GitHub Issues: [Create an issue](https://github.com/your-username/url-organizer/issues)
- Documentation: README.md
- MongoDB Atlas Support: https://support.mongodb.com/

---

**Last Updated**: November 24, 2025
