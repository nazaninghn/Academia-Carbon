# Security Notes 🔒

Important security information for Academia Carbon.

## Default Credentials

⚠️ **WARNING**: This repository does NOT include default credentials for security reasons.

### First Time Setup

After installation, you MUST create your own admin user:

```bash
python manage.py create_email_user admin@yourdomain.com YourSecurePassword123! --first-name "Admin" --last-name "User"
```

## Password Requirements

### Minimum Requirements
- At least 8 characters
- Mix of uppercase and lowercase letters
- At least one number
- At least one special character
- Not similar to personal information
- Not a commonly used password

### Good Password Examples
- `MySecure#Pass2025!`
- `Academia@Carbon$123`
- `GHG*Tracker!2025`

### Bad Password Examples
❌ `password123`
❌ `admin123`
❌ `12345678`
❌ `qwerty`

## Environment Variables

### Never Commit These to Git

```bash
# .env file (add to .gitignore)
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host/db
```

### Generate Secure SECRET_KEY

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use online generator:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Production Deployment

### Required Changes

1. **Change SECRET_KEY**
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

2. **Set DEBUG = False**
   ```python
   DEBUG = False
   ```

3. **Configure ALLOWED_HOSTS**
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

4. **Use HTTPS**
   ```python
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

5. **Use PostgreSQL (not SQLite)**
   ```python
   DATABASES = {
       'default': dj_database_url.config()
   }
   ```

## User Management

### Creating Admin Users

**Development:**
```bash
python manage.py create_email_user admin@localhost.com DevPassword123! --first-name "Dev" --last-name "Admin"
```

**Production:**
```bash
python manage.py create_email_user admin@yourdomain.com $(openssl rand -base64 32) --first-name "Admin" --last-name "User"
```

### Removing Test Users

Before going to production, remove any test users:

```python
from django.contrib.auth.models import User
User.objects.filter(email__contains='test').delete()
User.objects.filter(email__contains='example.com').delete()
```

## Database Security

### Backup Encryption

Always encrypt database backups:

```bash
# Backup with encryption
pg_dump dbname | gpg --encrypt --recipient your@email.com > backup.sql.gpg

# Restore
gpg --decrypt backup.sql.gpg | psql dbname
```

### Connection Security

Use SSL for database connections:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}
```

## API Security

### Rate Limiting

Consider adding rate limiting:

```bash
pip install django-ratelimit
```

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m')
def login_view(request):
    # ...
```

### CORS Configuration

If using API, configure CORS properly:

```bash
pip install django-cors-headers
```

## Monitoring

### Security Monitoring

1. **Enable Django Security Middleware**
   - Already enabled in settings.py

2. **Monitor Failed Login Attempts**
   - Log failed attempts
   - Alert on suspicious activity

3. **Regular Security Audits**
   ```bash
   python manage.py check --deploy
   ```

### Logging

Configure secure logging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
```

## Incident Response

### If Credentials Are Compromised

1. **Immediately change all passwords**
2. **Rotate SECRET_KEY**
3. **Check logs for unauthorized access**
4. **Notify affected users**
5. **Review security measures**

### If Database Is Compromised

1. **Take system offline**
2. **Restore from clean backup**
3. **Change all credentials**
4. **Investigate breach**
5. **Implement additional security**

## Compliance

### GDPR Considerations

- User data encryption
- Right to be forgotten
- Data export functionality
- Privacy policy
- Cookie consent

### Data Retention

Configure data retention policies:

```python
# Delete old emission records
from datetime import timedelta
from django.utils import timezone
from ghg.models import EmissionRecord

cutoff_date = timezone.now() - timedelta(days=365*7)  # 7 years
EmissionRecord.objects.filter(created_at__lt=cutoff_date).delete()
```

## Security Checklist

### Before Deployment

- [ ] SECRET_KEY is secure and not in Git
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] Database uses PostgreSQL
- [ ] Strong passwords enforced
- [ ] No default credentials
- [ ] Security middleware enabled
- [ ] CSRF protection enabled
- [ ] XSS protection enabled
- [ ] SQL injection protection verified
- [ ] File upload restrictions
- [ ] Rate limiting configured
- [ ] Logging enabled
- [ ] Backups configured
- [ ] SSL certificates valid
- [ ] Dependencies updated
- [ ] Security audit completed

### Regular Maintenance

- [ ] Weekly: Review logs
- [ ] Monthly: Update dependencies
- [ ] Quarterly: Security audit
- [ ] Annually: Penetration testing

## Resources

### Security Tools

- **Django Security Check**: `python manage.py check --deploy`
- **Safety**: Check for known vulnerabilities
  ```bash
  pip install safety
  safety check
  ```
- **Bandit**: Security linter
  ```bash
  pip install bandit
  bandit -r .
  ```

### Documentation

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email: security@academiacarbon.org
3. Include:
   - Description
   - Steps to reproduce
   - Potential impact
   - Suggested fix

We will respond within 48 hours.

---

**Remember**: Security is everyone's responsibility! 🔒

**Last Updated**: November 24, 2025  
**Version**: 2.0.0
