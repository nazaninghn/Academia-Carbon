# Render Deployment Guide 🚀

This guide helps you deploy Academia Carbon to Render.com successfully.

## 🔧 Environment Variables

Set these environment variables in your Render dashboard:

### Required Variables
```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,.onrender.com

# Database (automatically set by Render)
DATABASE_URL=postgresql://user:pass@host:port/db

# Email Configuration (optional)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Optional Variables
```bash
# CSRF Protection
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com

# Admin Notifications
ADMIN_NOTIFICATION_EMAILS=admin@yourdomain.com
```

## 🚀 Deployment Steps

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub account

### 2. Create PostgreSQL Database
- Click "New +" → "PostgreSQL"
- Name: `academia-carbon-db`
- Plan: Free tier
- Note the connection details

### 3. Create Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Settings:
  - **Name**: `academia-carbon`
  - **Runtime**: `Python`
  - **Build Command**: `./build.sh`
  - **Start Command**: `gunicorn carbon_tracker.wsgi:application`
  - **Python Version**: `3.11.0`

### 4. Set Environment Variables
In your web service settings, add:

```bash
SECRET_KEY=generate-a-secure-key
DEBUG=False
ALLOWED_HOSTS=academia-carbon.onrender.com,.onrender.com
DATABASE_URL=[Link to your PostgreSQL database]
```

### 5. Deploy
- Click "Deploy Latest Commit"
- Monitor build logs for any errors

## 🔍 Troubleshooting

### Common Issues

#### 1. Internal Server Error (500)
**Symptoms**: White page with "Internal Server Error"

**Solutions**:
- Check build logs for missing dependencies
- Verify all environment variables are set
- Ensure `reportlab` is in requirements.txt
- Check database connection

#### 2. Static Files Not Loading
**Symptoms**: No CSS/JS, broken styling

**Solutions**:
- Verify `STATIC_ROOT` and `STATIC_URL` settings
- Check `collectstatic` runs in build.sh
- Ensure WhiteNoise is configured

#### 3. Database Connection Error
**Symptoms**: "Database connection failed"

**Solutions**:
- Verify `DATABASE_URL` environment variable
- Check PostgreSQL database is running
- Ensure migrations ran successfully

#### 4. Import Errors
**Symptoms**: "ModuleNotFoundError" in logs

**Solutions**:
- Add missing packages to `requirements.txt`
- Check Python version compatibility
- Verify all `__init__.py` files exist

### Debug Commands

Run these in Render shell (if available):

```bash
# Check Django configuration
python manage.py check --deploy

# Test database connection
python manage.py dbshell

# View migration status
python manage.py showmigrations

# Create admin user
python manage.py setup_production --admin-email admin@yourdomain.com
```

## 📊 Post-Deployment Setup

### 1. Create Admin User
```bash
# In Render shell or during first deployment
python manage.py setup_production
```

### 2. Load Sample Data (Optional)
```bash
python manage.py load_sample_data
```

### 3. Test Key Features
- [ ] User registration/login
- [ ] Emission calculations
- [ ] Analysis dashboard
- [ ] PDF report generation
- [ ] Static files loading

## 🔒 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] HTTPS enabled (automatic on Render)
- [ ] Database credentials secure
- [ ] Admin user created with strong password

## 📈 Performance Optimization

### 1. Database Optimization
- Use connection pooling
- Add database indexes for frequently queried fields
- Monitor query performance

### 2. Static Files
- Enable compression with WhiteNoise
- Use CDN for large static assets
- Optimize images and CSS

### 3. Caching
- Enable Django caching for expensive operations
- Cache API responses
- Use browser caching headers

## 🔄 Continuous Deployment

### GitHub Actions (Optional)
The project includes a CI/CD pipeline in `.github/workflows/ci.yml`:

- Runs tests on multiple Python versions
- Checks code quality with linting
- Creates deployment packages
- Runs security scans

### Manual Deployment
1. Push changes to GitHub
2. Render automatically detects changes
3. Builds and deploys new version
4. Monitor deployment logs

## 📞 Support

If you encounter issues:

1. **Check Render Logs**: View build and runtime logs in dashboard
2. **GitHub Issues**: Report bugs at repository issues page
3. **Documentation**: Review Django and Render documentation
4. **Community**: Ask questions in GitHub Discussions

## 🎯 Success Indicators

Your deployment is successful when:

- ✅ Build completes without errors
- ✅ Application loads at your Render URL
- ✅ User can register and login
- ✅ Dashboard displays correctly
- ✅ Emission calculations work
- ✅ PDF reports generate successfully
- ✅ No 500 errors in logs

---

**Happy Deploying!** 🚀🌍