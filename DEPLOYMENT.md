# Deployment Guide - URL Organizer

## Quick Start Deployment

Your Flask URL Organizer is now deployment-ready! Choose your preferred platform:

---

## 🚀 Vercel (Serverless - Recommended)

### Prerequisites
- MongoDB Atlas account (free tier works)
- GitHub repository with your code
- Vercel account

### Steps

1. **Prepare MongoDB Atlas**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a cluster (free tier is fine)
   - Get your connection string: `mongodb+srv://username:password@cluster.mongodb.net/`
   - **Important**: Add `0.0.0.0/0` to Network Access (or Vercel's IPs)

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Vercel"
   git push origin main
   ```

3. **Deploy on Vercel**
   - Visit [vercel.com](https://vercel.com) and sign in
   - Click "Add New" → "Project"
   - Import your `url-organizer` repository
   - Click "Deploy" (it will fail first - that's OK)

4. **Configure Environment Variables**
   - Go to Project Settings → Environment Variables
   - Add these variables:
     ```
     MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/url_organizer
     SECRET_KEY=your-super-secret-random-string-here
     ADMIN_USERNAME=admin
     ADMIN_PASSWORD_HASH=<your-generated-hash>
     FLASK_ENV=production
     ```
   
5. **Generate Admin Password Hash**
   ```bash
   python scripts/hash_password.py
   # Copy the hash to ADMIN_PASSWORD_HASH
   ```

6. **Redeploy**
   - Go to Deployments tab
   - Click "Redeploy" on the latest deployment
   - ✅ Your app should now be live!

7. **Access Your App**
   - Public catalog: `https://your-app.vercel.app/`
   - Admin login: `https://your-app.vercel.app/admin/login`
   - Default credentials: `admin` / `admin123` (change this!)

---

## 🚂 Railway

### Steps

1. **Create Railway Account**
   - Visit [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Deploy**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `url-organizer`
   - Railway auto-detects the Dockerfile

3. **Add Environment Variables**
   - Click on your service → Variables
   - Add the same variables as Vercel (above)

4. **Generate Domain**
   - Go to Settings → Generate Domain
   - Your app is live!

---

## 🎨 Render

### Steps

1. **Create Render Account**
   - Visit [render.com](https://render.com)
   - Sign up with GitHub

2. **New Web Service**
   - Click "New +" → "Web Service"
   - Connect your `url-organizer` repo
   - Render detects the configuration from `render.yaml`

3. **Configure**
   - Name: `url-organizer`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app --bind 0.0.0.0:$PORT`

4. **Environment Variables**
   - Add all the variables from the Vercel section

5. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment

---

## 🐳 Docker (Self-Hosted)

### Local Docker

```bash
# Build
docker build -t url-organizer .

# Run
docker run -p 8000:8000 \
  -e MONGO_URI="mongodb+srv://..." \
  -e SECRET_KEY="your-secret" \
  -e ADMIN_USERNAME="admin" \
  -e ADMIN_PASSWORD_HASH="your-hash" \
  -e FLASK_ENV="production" \
  url-organizer

# Access at http://localhost:8000
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGO_URI=${MONGO_URI}
      - SECRET_KEY=${SECRET_KEY}
      - ADMIN_USERNAME=${ADMIN_USERNAME}
      - ADMIN_PASSWORD_HASH=${ADMIN_PASSWORD_HASH}
      - FLASK_ENV=production
    restart: unless-stopped

  # Optional: Local MongoDB
  # mongo:
  #   image: mongo:7
  #   ports:
  #     - "27017:27017"
  #   volumes:
  #     - mongo-data:/data/db

# volumes:
#   mongo-data:
```

Run with:
```bash
docker-compose up -d
```

---

## 🔧 Post-Deployment Checklist

- [ ] MongoDB Atlas network access configured
- [ ] All environment variables set
- [ ] Admin password hash generated and set
- [ ] SECRET_KEY is a strong random string
- [ ] Can access public catalog
- [ ] Can login to admin panel
- [ ] Can create/edit/delete URLs
- [ ] Search and tag filtering works
- [ ] Health check endpoint works (`/health`)

---

## 🔐 Security Best Practices

1. **Change Default Password**
   ```bash
   python scripts/hash_password.py
   # Use a strong password, update ADMIN_PASSWORD_HASH
   ```

2. **Rotate SECRET_KEY**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   # Update SECRET_KEY in your deployment
   ```

3. **MongoDB Security**
   - Use MongoDB Atlas (managed, secure)
   - Enable authentication
   - Restrict network access to your deployment IPs
   - Use strong passwords

4. **HTTPS Only**
   - All major platforms (Vercel, Railway, Render) provide HTTPS automatically
   - Never deploy without HTTPS in production

---

## 🐛 Troubleshooting

### "MongoDB connection failed"
- Check `MONGO_URI` is correct
- Verify MongoDB Atlas network access (whitelist 0.0.0.0/0 for serverless)
- Ensure credentials are correct in connection string

### "Invalid username or password" (admin login)
- Verify `ADMIN_PASSWORD_HASH` matches your password
- Regenerate hash: `python scripts/hash_password.py`
- Check `ADMIN_USERNAME` environment variable

### "502 Bad Gateway" or timeout errors
- Increase timeout in deployment settings (120s recommended)
- Check MongoDB connection latency
- Verify all environment variables are set

### App starts but shows errors
- Check deployment logs
- Verify `/health` endpoint returns 200
- Test MongoDB connection separately

---

## 📊 Monitoring

### Health Check
```bash
curl https://your-app.vercel.app/health
```

Response:
```json
{
  "status": "ok",
  "database": "connected"
}
```

### Logs
- **Vercel**: Deployments → Select deployment → Logs
- **Railway**: Service → Logs tab
- **Render**: Service → Logs tab
- **Docker**: `docker logs <container-id>`

---

## 🎉 Success!

Your URL Organizer is now live! 

- **Username**: `admin` (or your custom username)
- **Password**: `admin123` (or your custom password)

**Important**: Change the default password immediately after first login!

---

## 📝 Next Steps

1. Add your first URLs via the admin dashboard
2. Organize them with tags
3. Share the public catalog URL with others
4. Customize the styling if needed
5. Consider adding more features from the roadmap

Enjoy your deployed URL Organizer! 🚀
