# Security Quick Reference Guide

## 🚀 Quick Setup (5 Minutes)

### 1. Get reCAPTCHA Keys
```
1. Visit: https://www.google.com/recaptcha/admin
2. Click "+" to create new site
3. Select "reCAPTCHA v3"
4. Add domains: localhost, 127.0.0.1, yourdomain.com
5. Copy Site Key and Secret Key
```

### 2. Configure Environment
```bash
# Edit .env file
RECAPTCHA_SITE_KEY=your_site_key_here
RECAPTCHA_SECRET_KEY=your_secret_key_here
RECAPTCHA_ENABLED=True
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Test
```bash
python manage.py test ghg.tests_captcha
```

---

## 🔒 Security Features

| Feature | Status | Protection Against |
|---------|--------|-------------------|
| Email Uniqueness | ✅ | Duplicate accounts |
| Account Lockout | ✅ | Brute force attacks |
| reCAPTCHA v3 | ✅ | Bot attacks |
| Security Logging | ✅ | Unauthorized access |

---

## 📊 Configuration

### Account Lockout
```python
MAX_FAILED_ATTEMPTS = 5      # Failed attempts before lockout
LOCKOUT_DURATION = 1800      # 30 minutes in seconds
```

### reCAPTCHA
```python
RECAPTCHA_SCORE_THRESHOLD = 0.5   # Default (0.0=bot, 1.0=human)
RECAPTCHA_STRICT_THRESHOLD = 0.7  # For sensitive operations
```

---

## 🛠️ Common Commands

### Unlock Account
```bash
# Unlock by email
python manage.py unlock_account user@example.com

# Unlock by IP
python manage.py unlock_account 192.168.1.1
```

### Fix Duplicate Emails
```bash
# Fix existing duplicates
python manage.py fix_duplicate_emails

# Add unique constraint
python manage.py make_email_unique
```

### View Logs
```bash
# Watch security logs in real-time
tail -f logs/security.log

# Search for specific user
grep "user@example.com" logs/security.log

# Count failed logins today
grep "login_failed" logs/security.log | grep "$(date +%Y-%m-%d)" | wc -l
```

---

## 🔍 Monitoring

### Key Metrics to Watch

1. **Failed Login Rate**
   - Normal: <5% of total logins
   - Alert if: >10%

2. **reCAPTCHA Scores**
   - Normal: Average >0.7
   - Alert if: Average <0.5

3. **Locked Accounts**
   - Normal: <1% of active users
   - Alert if: >5%

4. **Bot Detection**
   - Normal: 95%+ detection rate
   - Alert if: <90%

---

## 🚨 Troubleshooting

### Users Can't Login

**Symptom**: "Account temporarily locked" message

**Solution**:
```bash
python manage.py unlock_account user@example.com
```

### reCAPTCHA Not Working

**Symptom**: "Security verification failed" on every login

**Check**:
1. Keys configured in `.env`?
2. Domain registered in reCAPTCHA console?
3. `RECAPTCHA_ENABLED=True`?

**Quick Fix**:
```bash
# Temporarily disable for testing
RECAPTCHA_ENABLED=False
```

### Too Many False Positives

**Symptom**: Legitimate users blocked by reCAPTCHA

**Solution**: Lower threshold in `ghg/captcha.py`:
```python
RECAPTCHA_SCORE_THRESHOLD = 0.3  # More lenient
```

---

## 📝 Security Checklist

### Before Deployment

- [ ] `SECRET_KEY` is strong and unique
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` configured
- [ ] reCAPTCHA keys configured
- [ ] HTTPS enabled
- [ ] Security logs monitored
- [ ] Backup strategy in place

### After Deployment

- [ ] Test login/signup works
- [ ] Test account lockout works
- [ ] Test reCAPTCHA works
- [ ] Monitor security logs
- [ ] Set up alerts
- [ ] Document incident response

---

## 📚 Documentation

- **Full Guide**: `SECURITY_IMPLEMENTATION_SUMMARY.md`
- **Email Uniqueness**: `SECURITY_EMAIL_UNIQUE.md`
- **Account Lockout**: `SECURITY_ACCOUNT_LOCKOUT.md`
- **reCAPTCHA**: `SECURITY_CAPTCHA.md`

---

## 🆘 Emergency Contacts

### Unlock All Accounts
```python
# In Django shell
from django.core.cache import cache
cache.clear()  # Clears all lockouts
```

### Disable reCAPTCHA
```bash
# In .env
RECAPTCHA_ENABLED=False
```

### Reset Failed Attempts
```python
# In Django shell
from ghg.security import AccountLockout
AccountLockout.reset_failed_attempts('user@example.com')
```

---

## 📞 Support

- **Security Issues**: security@academiacarbon.com
- **Documentation**: Check `SECURITY_*.md` files
- **Logs**: `logs/security.log`

---

**Last Updated**: January 14, 2024  
**Version**: 1.0  
**Status**: ✅ Production Ready
