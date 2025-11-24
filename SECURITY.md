# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do NOT** open a public issue
2. Email the details to: security@academiacarbon.org (or your contact)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Time

- We aim to respond within 48 hours
- We will provide updates every 7 days
- We will credit you in the fix (unless you prefer to remain anonymous)

## Security Best Practices

### For Deployment

1. **Change SECRET_KEY**
   ```python
   # In production, use environment variable
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

5. **Use Strong Passwords**
   - Minimum 8 characters
   - Mix of letters, numbers, symbols
   - Not similar to personal info

6. **Regular Updates**
   ```bash
   pip install --upgrade django
   ```

### For Users

1. Use strong, unique passwords
2. Enable two-factor authentication (when available)
3. Keep your email secure
4. Log out after use on shared computers
5. Report suspicious activity

## Known Security Features

- ✅ Password hashing with Django's PBKDF2
- ✅ CSRF protection
- ✅ SQL injection protection
- ✅ XSS protection
- ✅ Clickjacking protection
- ✅ Session security

## Security Updates

We will announce security updates through:
- GitHub Security Advisories
- Release notes
- Email notifications (for critical issues)

## Scope

This security policy applies to:
- Academia Carbon web application
- All official releases
- Documentation

## Out of Scope

- Third-party dependencies (report to their maintainers)
- Issues in forked versions
- Social engineering attacks

Thank you for helping keep Academia Carbon secure! 🔒
