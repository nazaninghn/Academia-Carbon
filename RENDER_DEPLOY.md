# Deploy to Render.com 🚀

Complete guide to deploy Academia Carbon on Render.com.

## Prerequisites

- GitHub account
- Render.com account (free tier available)
- Project pushed to GitHub

---

## Step 1: Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

---

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

---

## Step 3: Create PostgreSQL Database

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `academia-carbon-db`
   - **Database**: `academia_carbon`
   - **User**: `academia_carbon_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)
3. Click **"Create Database"**
4. Wait for database to be created
5. **Copy the Internal Database URL** (you'll need this)

---

## Step 4: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:

### Basic Settings
- **Name**: `academia-carbon`
- **Region**: Same as database
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`

### Build Settings
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn carbon_tracker.wsgi:application`

### Environment Variables
Click **"Add Environment Variable"** for each:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `SECRET_KEY` | (Click "Generate" button) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
| `DATABASE_URL` | (Paste Internal Database URL from Step 3) |

### Plan
- **Instance Type**: Free (or paid for production)

4. Click **"Create Web Service"**

---

## Step 5: Wait for Deployment

1. Render will:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start the server

2. Watch the logs for any errors

3. First deployment takes 5-10 minutes

---

## Step 6: Create Superuser

After deployment, you need to create an admin user:

1. Go to your service dashboard
2. Click **"Shell"** tab
3. Run:
```bash
python manage.py create_email_user admin@yourdomain.com YourPassword123 --first-name "Admin" --last-name "User"
```

Or use Django's createsuperuser:
```bash
python manage.py createsuperuser
```

---

## Step 7: Access Your Application

Your app will be available at:
```
https://your-app-name.onrender.com
```

---

## Environment Variables Explained

### Required Variables

**SECRET_KEY**
- Django secret key for security
- Use Render's "Generate" button
- Never commit this to Git

**DEBUG**
- Set to `False` in production
- Set to `True` only for debugging

**ALLOWED_HOSTS**
- Your Render domain: `your-app-name.onrender.com`
- Add custom domain if you have one
- Separate multiple hosts with commas

**DATABASE_URL**
- PostgreSQL connection string
- Provided by Render database
- Format: `postgresql://user:password@host:port/database`

### Optional Variables

**PYTHON_VERSION**
- Python version to use
- Default: `3.11.0`

---

## Custom Domain (Optional)

### 1. Add Custom Domain in Render

1. Go to your web service
2. Click **"Settings"**
3. Scroll to **"Custom Domains"**
4. Click **"Add Custom Domain"**
5. Enter your domain: `academiacarbon.com`

### 2. Configure DNS

Add these records to your DNS provider:

**For root domain (academiacarbon.com):**
```
Type: A
Name: @
Value: [Render's IP address]
```

**For www subdomain:**
```
Type: CNAME
Name: www
Value: your-app-name.onrender.com
```

### 3. Update ALLOWED_HOSTS

Add your custom domain to environment variables:
```
ALLOWED_HOSTS=your-app-name.onrender.com,academiacarbon.com,www.academiacarbon.com
```

---

## Troubleshooting

### Issue: Build Failed

**Check:**
- `requirements.txt` is correct
- `build.sh` has execute permissions
- Python version is compatible

**Solution:**
```bash
# Make build.sh executable
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### Issue: Static Files Not Loading

**Check:**
- `STATIC_ROOT` is set in settings.py
- `collectstatic` runs in build.sh
- WhiteNoise is installed

**Solution:**
Already configured in our settings.py!

### Issue: Database Connection Error

**Check:**
- `DATABASE_URL` environment variable is set
- Database is running
- Connection string is correct

**Solution:**
Copy the Internal Database URL from your Render database.

### Issue: 502 Bad Gateway

**Check:**
- Application is starting correctly
- Check logs for errors
- Gunicorn is running

**Solution:**
Check the logs in Render dashboard.

### Issue: ALLOWED_HOSTS Error

**Check:**
- `ALLOWED_HOSTS` includes your Render domain
- No typos in domain name

**Solution:**
```
ALLOWED_HOSTS=your-app-name.onrender.com
```

---

## Monitoring

### View Logs

1. Go to your service dashboard
2. Click **"Logs"** tab
3. View real-time logs

### Metrics

1. Click **"Metrics"** tab
2. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response time

---

## Updating Your Application

### 1. Make Changes Locally

```bash
# Make your changes
git add .
git commit -m "Your changes"
```

### 2. Push to GitHub

```bash
git push origin main
```

### 3. Automatic Deployment

Render will automatically:
- Detect the push
- Pull latest code
- Run build script
- Deploy new version

---

## Database Backups

### Manual Backup

1. Go to your database dashboard
2. Click **"Backups"** tab
3. Click **"Create Backup"**

### Automatic Backups

- Free tier: No automatic backups
- Paid tiers: Daily automatic backups

---

## Scaling

### Vertical Scaling (More Resources)

1. Go to service settings
2. Change **"Instance Type"**
3. Options:
   - Free: 512 MB RAM
   - Starter: 1 GB RAM ($7/month)
   - Standard: 2 GB RAM ($25/month)

### Horizontal Scaling (More Instances)

Available on paid plans:
1. Go to service settings
2. Increase **"Number of Instances"**

---

## Cost Estimation

### Free Tier
- Web Service: Free (with limitations)
- PostgreSQL: Free (90 days, then $7/month)
- **Total**: $0 for 90 days, then $7/month

### Starter Tier
- Web Service: $7/month
- PostgreSQL: $7/month
- **Total**: $14/month

### Production Tier
- Web Service: $25/month
- PostgreSQL: $25/month
- **Total**: $50/month

---

## Security Checklist

- [x] DEBUG = False
- [x] SECRET_KEY is generated and secure
- [x] ALLOWED_HOSTS is configured
- [x] Database uses PostgreSQL (not SQLite)
- [x] Static files served via WhiteNoise
- [x] HTTPS enabled (automatic on Render)
- [ ] Custom domain with SSL (optional)
- [ ] Environment variables not in Git
- [ ] Regular backups configured

---

## Performance Tips

### 1. Enable Caching

Add to settings.py:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}
```

### 2. Optimize Database Queries

Use `select_related()` and `prefetch_related()`.

### 3. Compress Static Files

Already configured with WhiteNoise!

### 4. Use CDN for Static Files

Consider using Cloudflare or AWS CloudFront.

---

## Maintenance

### Weekly
- Check logs for errors
- Monitor performance metrics
- Review database size

### Monthly
- Update dependencies
- Review security advisories
- Check backup status

### Quarterly
- Performance optimization
- Database cleanup
- Security audit

---

## Support

### Render Support
- Documentation: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### Academia Carbon
- GitHub Issues: https://github.com/yourusername/academia-carbon/issues
- Documentation: See README.md

---

## Quick Reference

### Useful Commands (in Render Shell)

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Check deployment
python manage.py check --deploy

# Load sample data
python manage.py load_sample_data
```

### Environment Variables Template

```
PYTHON_VERSION=3.11.0
SECRET_KEY=[generated]
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=[from-render-database]
```

---

## Success! 🎉

Your Academia Carbon application is now live on Render!

**Next Steps:**
1. Test all features
2. Create test users
3. Add your custom domain (optional)
4. Share with your team
5. Monitor performance

---

**Deployment Date**: November 24, 2025  
**Version**: 2.0.0  
**Status**: Production Ready ✅
