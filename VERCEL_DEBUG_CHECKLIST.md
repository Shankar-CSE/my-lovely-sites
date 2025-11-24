# Vercel Deployment Debug Checklist

## Step-by-Step Verification

### ✅ 1. Push Latest Changes
```bash
git push origin main
```
Wait for Vercel to auto-deploy (2-3 minutes)

---

### ✅ 2. Check Debug Endpoint

Visit: `https://your-app.vercel.app/debug`

**Expected Output:**
```json
{
  "environment_variables": {
    "MONGO_URI": "SET",
    "SECRET_KEY": "SET", 
    "ADMIN_USERNAME": "SET",
    "ADMIN_PASSWORD_HASH": "SET",
    "FLASK_ENV": "production"
  },
  "python_version": "3.x.x",
  "working_directory": "/var/task",
  "app_name": "app"
}
```

**If any show "NOT SET":**
1. Go to Vercel Dashboard
2. Project Settings → Environment Variables
3. Add the missing variable
4. Redeploy

---

### ✅ 3. Check Health Endpoint

Visit: `https://your-app.vercel.app/health`

**Expected Output:**
```json
{
  "status": "ok",
  "database": "connected"
}
```

**If "disconnected":**
- Check MongoDB Atlas Network Access has `0.0.0.0/0`
- Verify MONGO_URI format is correct
- Test connection string in MongoDB Compass

---

### ✅ 4. Check Home Page

Visit: `https://your-app.vercel.app/`

**Expected:** HTML page with "URL Catalog" heading

**If still getting 500 error:**
The error will now show detailed information:
```json
{
  "error": "actual error message",
  "type": "ErrorType",
  "path": "/",
  "method": "GET",
  "traceback": "full stack trace"
}
```

---

## Environment Variables - Quick Copy-Paste

### 1. MONGO_URI
```
mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/url_organizer?retryWrites=true&w=majority
```
- Replace USERNAME and PASSWORD
- Get from MongoDB Atlas → Connect → Connect your application

### 2. SECRET_KEY
Generate a new one:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. ADMIN_USERNAME
```
admin
```
(or your preferred username)

### 4. ADMIN_PASSWORD_HASH
```bash
source venv/bin/activate
python scripts/hash_password.py
```
Enter your password, copy the hash

### 5. FLASK_ENV
```
production
```

---

## MongoDB Atlas Network Access

1. Go to: https://cloud.mongodb.com/
2. Select your cluster
3. Click "Network Access" in left sidebar
4. Click "Add IP Address"
5. Click "Allow Access from Anywhere"
6. IP: `0.0.0.0/0`
7. Click "Confirm"

⚠️ **This is REQUIRED for Vercel** (serverless platforms need this)

---

## Vercel Logs

If errors persist, check logs:
1. Vercel Dashboard → Deployments
2. Click on latest deployment
3. Click "Runtime Logs" tab
4. Look for error messages

Common log errors:

| Error Message | Solution |
|---------------|----------|
| `MONGO_URI not found` | Add MONGO_URI environment variable |
| `Connection timeout` | Add 0.0.0.0/0 to MongoDB Network Access |
| `Authentication failed` | Check MongoDB username/password |
| `KeyError: 'SECRET_KEY'` | Add SECRET_KEY environment variable |
| `ModuleNotFoundError` | Check all files are in git repo |

---

## Testing Locally with Production Config

Test before deploying:
```bash
cd /home/shan/Desktop/url-organizer
source venv/bin/activate

# Set test environment variables
export FLASK_ENV=production
export MONGO_URI="your-mongodb-atlas-uri"
export SECRET_KEY="test-secret-key"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD_HASH="your-hash"

# Run the app
python run.py
```

Visit http://localhost:5000 - should work identically to Vercel

---

## Quick Fixes

### Fix 1: "All variables show NOT SET"
**Problem:** Environment variables not configured in Vercel
**Solution:** Go to Vercel Settings → Environment Variables → Add all 5

### Fix 2: "Database: disconnected"
**Problem:** MongoDB Atlas network access
**Solution:** Add 0.0.0.0/0 to Network Access whitelist

### Fix 3: "Wrong MONGO_URI format"
**Problem:** Using localhost URI instead of Atlas
**Solution:** Use `mongodb+srv://` format from Atlas

### Fix 4: "Admin login fails"
**Problem:** Wrong password hash
**Solution:** Regenerate with `python scripts/hash_password.py`

### Fix 5: "Still getting 500 error"
**Problem:** Unknown - need more info
**Solution:** 
1. Check `/debug` endpoint output
2. Check Vercel Runtime Logs
3. Share the error traceback

---

## Success Indicators

When everything works:
- ✅ `/debug` shows all variables "SET"
- ✅ `/health` shows `"database": "connected"`
- ✅ `/` shows HTML catalog page
- ✅ `/admin/login` shows login form
- ✅ Can login with admin credentials
- ✅ Can create/edit/delete URLs
- ✅ Dark mode toggle works

---

## Next Steps After Success

1. **Secure the /debug endpoint** (remove or protect it)
2. **Change default password** if using admin123
3. **Add your URLs** via admin dashboard
4. **Share public URL** with others
5. **Monitor with /health** endpoint (set up uptime monitoring)

---

**Need Help?**
Share the output of:
1. https://your-app.vercel.app/debug
2. https://your-app.vercel.app/health
3. Vercel Runtime Logs (screenshot)
