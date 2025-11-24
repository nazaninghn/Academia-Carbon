# Complete Deployment Guide for Render.com

## Prerequisites
- GitHub account with your code pushed
- Render.com account (free tier works)
- PostgreSQL database created on Render

## Step 1: Push to GitHub
```bash
git add .
git commit -m "Production ready deployment"
git push origin main
```

## Step 2: Create Web Service on Render

1. Go to https://dashboard.render.com
2. Click "New +" > "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: academia-carbon (or your choice)
   - **Runtime**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn carbon_tracker.wsgi:application`

## Step 3: Set Environment Variables

In Render Dashboard > Environment, add:

```
DEBUG=False
SECRET_KEY=(click "Generate" button)
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=(auto-filled from database)
```

**Important:** Add your specific Render URL:
```
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```

Replace `your-app-name` with your actual Render service name.

## Step 4: Create PostgreSQL Database

1. In Render Dashboard, click "New +" > "PostgreSQL"
2. Name it: `academia-carbon-db`
3. Select free tier
4. Click "Create Database"
5. Copy the "Internal Database URL"
6. Go back to your Web Service > Environment
7. Add: `DATABASE_URL=(paste the URL)`

## Step 5: Deploy

1. Click "Manual Deploy" > "Deploy latest commit"
2. Wait 3-5 minutes for build to complete
3. Check logs for any errors

## Step 6: Run Post-Deployment Commands

After successful deployment, open Shell in Render Dashboard:

```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

Or create user via Python:
```python
from django.contrib.auth.models import User
User.objects.create_superuser(
    username='admin@example.com',
    email='admin@example.com',
    password='YourSecurePassword123'
)
```

## Step 7: Test Your Deployment

Visit: `https://your-app-name.onrender.com/en/login/`

Test:
- [ ] Page loads without errors
- [ ] CSS and JavaScript load correctly
- [ ] Login works with email
- [ ] Dashboard displays after login
- [ ] Responsive design works on mobile

## Troubleshooting 500 Errors

### Check Logs First
Render Dashboard > Your Service > Logs

Look for Python errors and tracebacks.

### Common Issues:

**1. DisallowedHost Error**
```
ALLOWED_HOSTS=.onrender.com,your-app-name.onrender.com
```

**2. CSRF Verification Failed**
```
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```

**3. Static Files Not Found**
```bash
python manage.py collectstatic --noinput
```

**4. Database Connection Error**
- Check DATABASE_URL is set
- Verify PostgreSQL database is running
- Check database credentials

**5. Module Not Found**
- Check all dependencies in `requirements.txt`
- Redeploy with "Clear build cache"

### Force Redeploy
1. Go to Render Dashboard
2. Click "Manual Deploy"
3. Select "Clear build cache & deploy"

## Environment Variables Reference

| Variable | Value | Required |
|----------|-------|----------|
| DEBUG | False | Yes |
| SECRET_KEY | (auto-generated) | Yes |
| ALLOWED_HOSTS | .onrender.com | Yes |
| DATABASE_URL | (from PostgreSQL) | Yes |
| CSRF_TRUSTED_ORIGINS | https://your-app.onrender.com | Yes |

## Post-Deployment Checklist

- [ ] Service deployed successfully
- [ ] Database connected
- [ ] Migrations completed
- [ ] Static files collected
- [ ] Superuser created
- [ ] Login page accessible
- [ ] Authentication works
- [ ] Dashboard loads
- [ ] Responsive on mobile
- [ ] No console errors

## Updating Your Deployment

When you make changes:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically detect and deploy changes.

## Free Tier Limitations

- Service sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month free
- Upgrade to paid plan ($7/month) for always-on service

## Support Resources

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Render Status: https://status.render.com

## Success!

Your application should now be live at:
```
https://your-app-name.onrender.com
```

Login with the superuser credentials you created.
