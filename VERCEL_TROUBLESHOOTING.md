# Vercel Deployment Troubleshooting Guide

## ✅ Fixed Issues

The `api/index.py` has been updated to:
- Use production configuration
- Add proper error handling
- Show detailed error messages if startup fails

## 🔧 Quick Fix Checklist

### 1. Environment Variables (Most Common Issue)

Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

You need **ALL 5** of these:

| Variable | Example Value | How to Generate |
|----------|--------------|-----------------|
| `MONGO_URI` | `mongodb+srv://user:pass@cluster.mongodb.net/url_organizer?retryWrites=true&w=majority` | MongoDB Atlas connection string |
| `SECRET_KEY` | `a1b2c3d4e5f6...` (64 chars) | `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ADMIN_USERNAME` | `admin` | Choose your username |
| `ADMIN_PASSWORD_HASH` | `$argon2id$v=19$m=...` | `python scripts/hash_password.py` |
| `FLASK_ENV` | `production` | Set manually |

⚠️ **After adding/changing variables, you MUST redeploy!**

### 2. MongoDB Atlas Network Access

**Required for Vercel (Serverless):**

1. Go to MongoDB Atlas Dashboard
2. Click **Network Access** in left sidebar
3. Click **Add IP Address**
4. Select **Allow Access from Anywhere**
5. Enter `0.0.0.0/0`
6. Click **Confirm**

Without this, you'll get connection timeout errors.

### 3. Redeploy After Changes

After fixing issues:
```bash
git add .
git commit -m "Fix Vercel deployment"
git push origin main
```

Vercel will auto-deploy, or manually trigger:
- Go to **Deployments** tab
- Click **•••** on latest deployment
- Click **Redeploy**

## 🔍 How to Read Vercel Logs

### Access Logs:
1. Go to your Vercel project
2. Click **Deployments** tab
3. Click on the latest deployment
4. Click **Runtime Logs** or **Build Logs**

### Common Error Messages & Solutions:

#### Error: "MONGO_URI not found" or "None"
```
KeyError: 'MONGO_URI'
```
**Solution**: Add `MONGO_URI` environment variable in Vercel settings

#### Error: "Connection timeout" or "Connection refused"
```
ServerSelectionTimeoutError: cluster.mongodb.net:27017
```
**Solution**: Add `0.0.0.0/0` to MongoDB Atlas Network Access

#### Error: "Authentication failed"
```
Authentication failed
```
**Solution**: Check MongoDB credentials in `MONGO_URI` are correct

#### Error: "Module not found"
```
ModuleNotFoundError: No module named 'app'
```
**Solution**: 
- Updated `api/index.py` should fix this
- Ensure all files are committed to git
- Check that `app/` folder exists in repository

#### Error: "Template not found"
```
jinja2.exceptions.TemplateNotFound: base.html
```
**Solution**: 
- Ensure `app/templates/` folder is in git
- Check `.gitignore` doesn't exclude templates
- Run: `git add app/templates/ && git commit -m "Add templates" && git push`

#### Error: "SECRET_KEY not set"
```
RuntimeError: The session is unavailable because no secret key was set
```
**Solution**: Add `SECRET_KEY` environment variable

## 🧪 Test Your Deployment

### 1. Health Check Endpoint
```bash
curl https://your-app.vercel.app/health
```

**Expected Response (Success):**
```json
{
  "status": "ok",
  "database": "connected"
}
```

**Error Response (If Issues):**
```json
{
  "status": "error",
  "message": "Connection timeout to cluster.mongodb.net:27017"
}
```

### 2. Home Page
```bash
curl https://your-app.vercel.app/
```
Should return HTML content

### 3. Admin Login Page
```bash
curl https://your-app.vercel.app/admin/login
```
Should return login form HTML

## 🐛 Still Getting 500 Internal Server Error?

### Step-by-Step Debug:

1. **Check Build Logs First**
   - Deployments → Your deployment → Build Logs
   - Look for Python package installation errors

2. **Check Runtime Logs**
   - Deployments → Your deployment → Runtime Logs  
   - Look for error messages when app starts

3. **Test Health Endpoint**
   ```bash
   curl https://your-app.vercel.app/health
   ```
   This will show the specific error message

4. **Verify All Environment Variables**
   - Settings → Environment Variables
   - Check all 5 are present
   - No typos in variable names
   - Values are not empty

5. **Test MongoDB Connection Separately**
   ```bash
   # In your local terminal with venv activated
   python -c "
   from pymongo import MongoClient
   import os
   client = MongoClient('YOUR_MONGO_URI_HERE')
   print(client.admin.command('ping'))
   "
   ```

6. **Check Git Repository**
   ```bash
   # Make sure all files are committed
   git status
   
   # Check these folders exist
   ls -la app/
   ls -la app/templates/
   ls -la app/routes/
   ```

## 📝 Deployment Checklist

Before deploying, verify:

- [ ] All files committed to git
- [ ] `api/index.py` updated (done ✓)
- [ ] `app/` folder in repository
- [ ] `app/templates/` folder in repository
- [ ] `requirements.txt` in repository
- [ ] `vercel.json` in repository
- [ ] MongoDB Atlas cluster created
- [ ] Network access set to 0.0.0.0/0
- [ ] All 5 environment variables set in Vercel
- [ ] Pushed latest changes to GitHub
- [ ] Triggered redeploy in Vercel

## 🎯 Expected Deployment Flow

1. **Build Phase** (1-2 minutes)
   - Installing Python packages
   - Installing dependencies from requirements.txt
   - ✓ Build completed

2. **Deploy Phase** (30 seconds)
   - Deploying to serverless functions
   - ✓ Deployment ready

3. **Runtime Phase**
   - First request initializes app
   - Connects to MongoDB
   - ✓ Application running

## 💡 Pro Tips

### Faster Debugging
Add this to `api/index.py` temporarily to see exact errors:
```python
import traceback

try:
    from app import create_app
    app = create_app('production')
except Exception as e:
    print("STARTUP ERROR:", str(e))
    print("TRACEBACK:", traceback.format_exc())
    raise
```

### Test Locally First
```bash
# Test with production config locally
FLASK_ENV=production python run.py

# Or test the api/index.py file
cd api && python index.py
```

### Monitor Your App
- Use Vercel Analytics (free)
- Check /health endpoint regularly
- Set up uptime monitoring (UptimeRobot, etc.)

## 🆘 Getting More Help

If still stuck, gather this info:

1. **Vercel Build Logs** (copy/paste the error)
2. **Vercel Runtime Logs** (copy/paste the error)
3. **Health endpoint response**: `curl https://your-app.vercel.app/health`
4. **Environment variables** (list names only, not values!)
5. **MongoDB Atlas region** and **Vercel deployment region**

Share this information for faster troubleshooting.

---

**Last Updated**: November 24, 2025  
**Status**: Ready for deployment 🚀
