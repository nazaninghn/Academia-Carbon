# Deployment Checklist - Version 2.1.0

## Pre-Deployment Steps

### 1. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 2. Check for Errors
```bash
python manage.py check --deploy
```

### 3. Test Locally
```bash
python manage.py runserver
```
Test all new features:
- On-Road DESNZ 2024
- Fugitive Emissions (all 5 sources)
- Mobile responsiveness

### 4. Database (No Migration Needed)
No database changes in this version - only emission factors updated.

## Deployment Steps

### For Render.com

#### 1. Update Environment Variables
Make sure these are set in Render dashboard:
```
PYTHON_VERSION=3.11.0
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.onrender.com
DATABASE_URL=postgresql://...
```

#### 2. Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

#### 3. Start Command
```bash
gunicorn carbon_tracker.wsgi:application
```

### For Other Platforms

#### Heroku
```bash
git push heroku main
heroku run python manage.py collectstatic --noinput
```

#### DigitalOcean/VPS
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## Post-Deployment Verification

### 1. Check Static Files
- [ ] CSS loads correctly
- [ ] JavaScript works
- [ ] Mobile CSS loads
- [ ] Icons display

### 2. Test New Features
- [ ] On-Road DESNZ 2024 calculations work
- [ ] Fugitive Emissions (R-410A, R-432A, R-22, Methane, R-600A)
- [ ] Supplier dropdown populates
- [ ] Forms submit correctly

### 3. Mobile Testing
- [ ] Open on mobile device
- [ ] Hamburger menu works
- [ ] Forms are usable
- [ ] Tables display correctly
- [ ] No horizontal scroll

### 4. API Endpoints
Test calculation endpoint:
```bash
curl -X POST https://your-domain.com/api/calculate/ \
  -H "Content-Type: application/json" \
  -d '{"category":"fugitive","source":"r432a","activity_data":10,"country":"global"}'
```

## Common Issues & Solutions

### Issue 1: Static Files Not Loading
**Symptoms:** CSS/JS not working, broken layout

**Solution:**
```bash
python manage.py collectstatic --noinput --clear
```

Check `settings.py`:
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

### Issue 2: Calculation Returns Error
**Symptoms:** "Cannot calculate" or 500 error

**Check:**
1. Browser console for JavaScript errors
2. Server logs for Python errors
3. CSRF token is present

**Debug:**
```python
# In views.py, add logging
import logging
logger = logging.getLogger(__name__)

@login_required
def calculate_emission(request):
    logger.info(f"Calculate request: {request.body}")
    # ... rest of code
```

### Issue 3: Mobile Layout Broken
**Symptoms:** Layout doesn't respond, elements overlap

**Solution:**
1. Clear browser cache
2. Check mobile.css is loaded:
```html
<link rel="stylesheet" href="{% static 'css/mobile.css' %}">
```
3. Verify viewport meta tag:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### Issue 4: CSRF Token Missing
**Symptoms:** 403 Forbidden on form submit

**Solution:**
Check `settings.py`:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://your-domain.onrender.com',
    'https://your-domain.com',
]
```

### Issue 5: Import Error for Emission Factors
**Symptoms:** "Module not found" or "Cannot import"

**Solution:**
```bash
# Restart server
sudo systemctl restart gunicorn

# Or on Render, trigger manual deploy
```

## Rollback Plan

If deployment fails:

### Quick Rollback
```bash
git revert HEAD
git push origin main
```

### Full Rollback to v2.0.0
```bash
git reset --hard <commit-hash-of-v2.0.0>
git push origin main --force
```

## Monitoring

### Check Logs
```bash
# Render
View logs in Render dashboard

# Heroku
heroku logs --tail

# VPS
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/nginx/error.log
```

### Performance
- [ ] Page load time < 3 seconds
- [ ] API response time < 1 second
- [ ] Mobile performance good (Lighthouse score > 80)

## Security Checklist

- [ ] DEBUG=False in production
- [ ] SECRET_KEY is secure and not in git
- [ ] ALLOWED_HOSTS configured
- [ ] CSRF_TRUSTED_ORIGINS set
- [ ] HTTPS enabled
- [ ] Security headers configured

## Success Criteria

✅ All pages load without errors
✅ Static files serve correctly
✅ New emission calculations work
✅ Mobile layout responsive
✅ No console errors
✅ Forms submit successfully
✅ User authentication works
✅ Database queries efficient

---

**Version:** 2.1.0  
**Deployment Date:** ___________  
**Deployed By:** ___________  
**Status:** ⬜ Success / ⬜ Failed / ⬜ Rolled Back
