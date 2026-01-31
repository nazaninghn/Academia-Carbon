# 🚀 Arcjet Integration - Step by Step

## You're at Arcjet Dashboard! Here's what to do:

### Step 1: Get Your API Key from Arcjet Dashboard

1. ✅ You're already at the "Install the Arcjet SDK" page
2. Choose **Python FastAPI** (closest to Django)
3. Copy your API key (starts with `ajkey_`)
4. Save it somewhere safe

### Step 2: Add API Key to Render

1. Go to https://dashboard.render.com
2. Select your service: `academia-carbon`
3. Click **Environment** tab
4. Add new environment variable:
   ```
   Key: ARCJET_KEY
   Value: ajkey_your_actual_key_here
   ```
5. Click **Save Changes**

### Step 3: Install Arcjet SDK

On your local machine:

```bash
cd Academia-Carbon
pip install arcjet-python
```

Update `requirements.txt`:
```bash
echo "arcjet-python>=1.0.0" >> requirements.txt
```

### Step 4: Update Settings

In `carbon_tracker/settings.py`, change the middleware:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'ghg.arcjet_simulation.ArcjetSimulatorMiddleware',  # OLD - Comment out
    'ghg.arcjet_real.ArcjetMiddleware',  # NEW - Use real Arcjet
    'ghg.middleware.SecurityHeadersMiddleware',
    # ... rest of middleware
]
```

### Step 5: Update Views

In `ghg/views.py`, change the import:

```python
# OLD
# from .arcjet_simulation import arcjet_protect

# NEW
from .arcjet_real import arcjet_protect
```

### Step 6: Test Locally

```bash
# Set environment variable
export ARCJET_KEY=ajkey_your_key_here

# Run server
python manage.py runserver
```

Try to login multiple times rapidly - you should see rate limiting!

### Step 7: Deploy to Render

```bash
git add .
git commit -m "Integrate real Arcjet security"
git push origin main
```

Render will automatically deploy with the new ARCJET_KEY.

### Step 8: Verify in Arcjet Dashboard

1. Go back to https://app.arcjet.com
2. Click on your site
3. You should see real-time requests
4. Try making requests to your site
5. Watch them appear in the dashboard!

---

## Quick Commands

### Install Arcjet
```bash
pip install arcjet-python
```

### Test Rate Limiting
```bash
# Make 10 rapid requests
for i in {1..10}; do
  curl https://academia-carbon.onrender.com/en/login/
done
```

### Check if Arcjet is Working
```bash
python manage.py security_status
```

---

## Troubleshooting

### "Arcjet not configured"
- Check ARCJET_KEY is set in Render environment
- Verify key starts with `ajkey_`
- Restart Render service

### "Module not found: arcjet"
- Run: `pip install arcjet-python`
- Add to requirements.txt
- Redeploy

### Too many blocks?
- Use `ARCJET_MODE=DRY_RUN` for testing
- Adjust rate limits in `arcjet_real.py`

---

## What You Get

✅ **Rate Limiting**: Automatic protection against brute force
✅ **Bot Detection**: ML-powered bot blocking
✅ **WAF**: Web Application Firewall
✅ **Dashboard**: Real-time security analytics
✅ **Alerts**: Email notifications for attacks

---

## Cost

Check your Arcjet plan:
- **Free Tier**: 100,000 requests/month
- **Pro**: Unlimited requests, advanced features

---

**Next:** Copy your API key from Arcjet dashboard and add it to Render!
