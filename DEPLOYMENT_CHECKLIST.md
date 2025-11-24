# Deployment Checklist ✅

Complete checklist for deploying Academia Carbon to Render.com.

## Pre-Deployment

### Code Preparation
- [x] All features tested locally
- [x] No hardcoded secrets in code
- [x] Database migrations created
- [x] Static files configured
- [x] Error handling implemented
- [x] Logging configured

### Files Created
- [x] `requirements.txt` - Updated with production dependencies
- [x] `build.sh` - Build script for Render
- [x] `render.yaml` - Render configuration
- [x] `.env.example` - Environment variables template
- [x] `.gitignore` - Updated with .env and render files
- [x] `RENDER_DEPLOY.md` - Deployment guide

### Settings Updated
- [x] `SECRET_KEY` from environment variable
- [x] `DEBUG` from environment variable
- [x] `ALLOWED_HOSTS` from environment variable
- [x] Database configuration with dj-database-url
- [x] WhiteNoise middleware added
- [x] Static files configuration
- [x] STATIC_ROOT configured

### Dependencies Added
- [x] gunicorn - WSGI server
- [x] psycopg2-binary - PostgreSQL adapter
- [x] whitenoise - Static file serving
- [x] dj-database-url - Database URL parsing
- [x] python-decouple - Environment variables

---

## GitHub

### Repository
- [ ] Code pushed to GitHub
- [ ] Repository is public or accessible to Render
- [ ] README.md updated
- [ ] LICENSE file added
- [ ] .gitignore configured

### Commit
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

---

## Render.com Setup

### Account
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Payment method added (if using paid tier)

### Database
- [ ] PostgreSQL database created
- [ ] Database name: `academia-carbon-db`
- [ ] Internal Database URL copied
- [ ] Database is running

### Web Service
- [ ] Web service created
- [ ] Repository connected
- [ ] Build command: `./build.sh`
- [ ] Start command: `gunicorn carbon_tracker.wsgi:application`
- [ ] Python version: 3.11.0

### Environment Variables
- [ ] `SECRET_KEY` - Generated
- [ ] `DEBUG` - Set to False
- [ ] `ALLOWED_HOSTS` - Set to Render domain
- [ ] `DATABASE_URL` - Set to database URL
- [ ] `PYTHON_VERSION` - Set to 3.11.0

---

## Post-Deployment

### Verification
- [ ] Application deployed successfully
- [ ] No errors in logs
- [ ] Homepage loads correctly
- [ ] Static files loading
- [ ] Database connected

### Admin Setup
- [ ] Superuser created
- [ ] Test login works
- [ ] Admin panel accessible

### Testing
- [ ] Login page works
- [ ] Signup page works
- [ ] Email authentication works
- [ ] Emission calculator works
- [ ] History page works
- [ ] All pages responsive

### Security
- [ ] HTTPS enabled (automatic on Render)
- [ ] DEBUG is False
- [ ] SECRET_KEY is secure
- [ ] ALLOWED_HOSTS configured
- [ ] No sensitive data in logs

---

## Optional Enhancements

### Custom Domain
- [ ] Domain purchased
- [ ] DNS configured
- [ ] Domain added in Render
- [ ] SSL certificate issued
- [ ] ALLOWED_HOSTS updated

### Monitoring
- [ ] Error tracking setup (e.g., Sentry)
- [ ] Performance monitoring
- [ ] Uptime monitoring
- [ ] Log aggregation

### Backups
- [ ] Database backup strategy
- [ ] Automated backups configured
- [ ] Backup restoration tested

### Email
- [ ] Email service configured (e.g., SendGrid)
- [ ] Email templates created
- [ ] Test emails sent

---

## Commands Reference

### Local Testing
```bash
# Test with production settings
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create test user
python manage.py create_email_user test@example.com password123
```

### Render Shell
```bash
# Create superuser
python manage.py createsuperuser

# Check deployment
python manage.py check --deploy

# View database tables
python manage.py dbshell
```

---

## Troubleshooting

### Build Fails
- [ ] Check build logs
- [ ] Verify requirements.txt
- [ ] Check Python version
- [ ] Verify build.sh permissions

### Application Won't Start
- [ ] Check start logs
- [ ] Verify gunicorn installed
- [ ] Check WSGI configuration
- [ ] Verify environment variables

### Static Files Missing
- [ ] Check STATIC_ROOT setting
- [ ] Verify WhiteNoise installed
- [ ] Check collectstatic ran
- [ ] Verify STATICFILES_STORAGE

### Database Errors
- [ ] Check DATABASE_URL
- [ ] Verify database is running
- [ ] Check migrations ran
- [ ] Verify database credentials

---

## Performance Checklist

### Optimization
- [ ] Database queries optimized
- [ ] Static files compressed
- [ ] Images optimized
- [ ] Caching configured
- [ ] CDN setup (optional)

### Monitoring
- [ ] Response times acceptable
- [ ] Memory usage normal
- [ ] CPU usage normal
- [ ] No memory leaks

---

## Security Checklist

### Django Security
- [ ] DEBUG = False
- [ ] SECRET_KEY secure
- [ ] ALLOWED_HOSTS configured
- [ ] CSRF protection enabled
- [ ] XSS protection enabled
- [ ] SQL injection protection

### HTTPS
- [ ] HTTPS enforced
- [ ] SECURE_SSL_REDIRECT = True (if needed)
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True

### Passwords
- [ ] Strong password requirements
- [ ] Password hashing enabled
- [ ] No default passwords

---

## Documentation

### Updated
- [ ] README.md
- [ ] INSTALLATION.md
- [ ] RENDER_DEPLOY.md
- [ ] CHANGELOG.md

### Created
- [ ] Deployment guide
- [ ] Environment variables guide
- [ ] Troubleshooting guide

---

## Final Steps

### Announcement
- [ ] Team notified
- [ ] Users notified
- [ ] Documentation shared
- [ ] Support channels ready

### Monitoring
- [ ] Set up alerts
- [ ] Monitor first 24 hours
- [ ] Check error rates
- [ ] Review performance

### Backup Plan
- [ ] Rollback procedure documented
- [ ] Previous version tagged
- [ ] Database backup created
- [ ] Emergency contacts ready

---

## Success Criteria

- ✅ Application accessible at Render URL
- ✅ All features working
- ✅ No errors in logs
- ✅ Performance acceptable
- ✅ Security measures in place
- ✅ Monitoring active
- ✅ Team can access
- ✅ Documentation complete

---

## Post-Launch

### Week 1
- [ ] Monitor daily
- [ ] Fix any issues
- [ ] Gather feedback
- [ ] Optimize performance

### Month 1
- [ ] Review metrics
- [ ] Plan improvements
- [ ] Update documentation
- [ ] Security review

---

**Deployment Status**: Ready ✅  
**Date**: November 24, 2025  
**Version**: 2.0.0  
**Platform**: Render.com
