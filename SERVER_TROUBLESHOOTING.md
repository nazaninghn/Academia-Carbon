# Server Troubleshooting Guide 🔧

## Issue: "Cannot Calculate" Error on Server

### Quick Fixes (Try These First)

#### 1. Collect Static Files
```bash
python manage.py collectstatic --noinput --clear
```

#### 2. Restart Server
```bash
# On Render
Trigger manual deploy or restart service

# On Heroku
heroku restart

# On VPS with Gunicorn
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

#### 3. Check Logs
```bash
# Render: View in dashboard
# Heroku: heroku logs --tail
# VPS: sudo tail -f /var/log/gunicorn/error.log
```

### Detailed Diagnostics

#### Check 1: Static Files
**Problem:** CSS/JS not loading

**Test:**
```bash
# Check if static files exist
ls staticfiles/css/
ls staticfiles/js/

# Should see:
# - style.css
# - mobile.css
# - charts.js
# - dashboard.js
```

**Fix:**
```bash
python manage.py collectstatic --noinput
```

#### Check 2: CSRF Token
**Problem:** 403 Forbidden on POST requests

**Test:** Open browser console, look for CSRF errors

**Fix in `settings.py`:**
```python
CSRF_TRUSTED_ORIGINS = [
    'https://your-domain.onrender.com',
    'https://www.your-domain.com',
]

# Also check:
CSRF_COOKIE_SECURE = True  # For HTTPS
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access
SESSION_COOKIE_SECURE = True
```

#### Check 3: JavaScript Errors
**Problem:** Calculate button doesn't work

**Test:** Open browser console (F12), check for errors

**Common Errors:**
1. `Uncaught ReferenceError: $ is not defined`
   - jQuery not loaded
   
2. `CSRF token missing`
   - Check form has `{% csrf_token %}`
   
3. `Cannot read property 'value' of null`
   - Element ID mismatch

**Fix:** Check browser console and fix specific error

#### Check 4: API Endpoint
**Problem:** /api/calculate/ returns 500 error

**Test:**
```bash
# From server
curl -X POST http://localhost:8000/api/calculate/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: your-token" \
  -d '{"category":"fugitive","source":"r432a","activity_data":10,"country":"global"}'
```

**Check Server Logs:**
```bash
# Look for Python errors
tail -f /var/log/gunicorn/error.log
```

#### Check 5: Database Connection
**Problem:** Database errors

**Test:**
```bash
python manage.py dbshell
# Should connect without errors
```

**Fix:**
Check `DATABASE_URL` environment variable

#### Check 6: Python Path
**Problem:** Import errors

**Test:**
```bash
python manage.py shell
>>> from ghg.emission_factors import calculate_emissions
>>> calculate_emissions('fugitive', 'r432a', 10, 'global')
```

**Fix:**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Environment Variables Checklist

Make sure these are set on server:

```bash
# Required
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.onrender.com,your-domain.com
DATABASE_URL=postgresql://...

# Optional but recommended
CSRF_TRUSTED_ORIGINS=https://your-domain.onrender.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Specific Error Messages

#### Error: "Please select an emission source"
**Cause:** JavaScript can't find source select element

**Fix:**
1. Check browser console for errors
2. Verify `fugitive-source` ID exists in HTML
3. Clear browser cache
4. Check mobile.css is loaded

#### Error: "Activity data must be positive"
**Cause:** Form validation failing

**Fix:**
1. Check input has valid number
2. Verify min="0" attribute
3. Check JavaScript validation

#### Error: "CSRF verification failed"
**Cause:** CSRF token missing or invalid

**Fix:**
```python
# In settings.py
CSRF_TRUSTED_ORIGINS = [
    'https://your-domain.onrender.com',
]

# In template
{% csrf_token %}
```

#### Error: "Module 'ghg.emission_factors' has no attribute"
**Cause:** Code not deployed or Python cache issue

**Fix:**
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Restart server
sudo systemctl restart gunicorn
```

### Testing After Fix

#### 1. Test Locally First
```bash
python test_deployment.py
```

Should show:
```
✅ ALL TESTS PASSED - Deployment successful!
```

#### 2. Test on Server
```bash
# SSH into server
ssh user@your-server

# Run test
cd /path/to/project
source venv/bin/activate
python test_deployment.py
```

#### 3. Test in Browser
1. Open DevTools (F12)
2. Go to Network tab
3. Try calculation
4. Check for:
   - 200 OK response
   - No console errors
   - Result displays

### Performance Issues

#### Slow Calculations
**Cause:** Database queries or large data

**Fix:**
```python
# Add database indexes
python manage.py makemigrations
python manage.py migrate

# Enable query optimization
DEBUG = False
```

#### Timeout Errors
**Cause:** Server timeout too short

**Fix:**
```python
# In gunicorn config
timeout = 120
workers = 4
```

### Still Not Working?

#### Get Detailed Logs
```bash
# Enable DEBUG temporarily (ONLY for testing)
DEBUG = True

# Check full error
python manage.py runserver

# Or check gunicorn logs
sudo journalctl -u gunicorn -n 100
```

#### Contact Support
Provide:
1. Error message (exact text)
2. Browser console screenshot
3. Server logs
4. Steps to reproduce

---

**Last Updated:** November 26, 2025  
**Version:** 2.1.0
