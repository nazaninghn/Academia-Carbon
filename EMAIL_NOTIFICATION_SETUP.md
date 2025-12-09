# Email Notification System

## Overview
Complete email notification system for Academia Carbon that sends notifications to admins when:
- New material requests are submitted
- Custom emission factors are added (optional)
- Material request status changes (to notify users)

## Features Implemented ✅

### 1. Admin Notifications
**When triggered:**
- User submits a new material request via "Request New Material" button
- Email sent immediately to all configured admin emails

**Email contains:**
- Material name and category
- User information (username, email)
- Description of the material
- Suggested emission factor (if provided)
- Direct link to admin panel for review

### 2. User Notifications
**When triggered:**
- Admin approves/rejects/updates material request status
- Email sent to the user who submitted the request

**Email contains:**
- Status update (Approved/Rejected/In Progress)
- Admin notes (if any)
- Next steps for the user

### 3. Custom Factor Notifications (Optional)
**When triggered:**
- User adds a custom emission factor
- Can be enabled for high-value factors needing verification

## Configuration

### Development Setup (Console Backend)

For development, emails are printed to the console. No configuration needed!

```bash
# .env file
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
ADMIN_NOTIFICATION_EMAILS=admin@example.com
SITE_URL=http://127.0.0.1:8000
```

### Production Setup (SMTP - Gmail Example)

#### Step 1: Create App Password (Gmail)
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Go to "App passwords"
4. Generate password for "Mail"
5. Copy the 16-character password

#### Step 2: Configure .env file
```bash
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=noreply@academiacarbon.com

# Admin emails (comma-separated for multiple admins)
ADMIN_NOTIFICATION_EMAILS=admin1@company.com,admin2@company.com

# Site URL (for links in emails)
SITE_URL=https://your-app.onrender.com
```

#### Step 3: Test Email Configuration
```bash
python manage.py test_email
```

### Other Email Providers

#### SendGrid
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

#### AWS SES
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-ses-smtp-username
EMAIL_HOST_PASSWORD=your-ses-smtp-password
```

#### Mailgun
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=postmaster@your-domain.mailgun.org
EMAIL_HOST_PASSWORD=your-mailgun-password
```

## Usage

### Testing Email System
```bash
# Test email configuration
python manage.py test_email

# Check console output in development
# Check inbox in production
```

### Manual Notification Sending (Python Shell)
```python
from ghg.models import MaterialRequest
from ghg.notifications import send_material_request_notification

# Get a material request
request = MaterialRequest.objects.first()

# Send notification
send_material_request_notification(request)
```

## Notification Flow

### Material Request Flow
```
1. User clicks "Request New Material"
2. Fills form and submits
3. MaterialRequest created in database
4. Email sent to all admins immediately
5. Admin receives email with direct link
6. Admin reviews in admin panel
7. Admin approves/rejects
8. Email sent to user with status update
```

### Email Content Examples

#### Admin Notification Email
```
Subject: [Academia Carbon] New Material Request: Bamboo Fiber

New Material Request Submitted

Material Name: Bamboo Fiber
Category: purchased-goods
Requested by: john_doe (john@company.com)
Description: We need emission factor for bamboo fiber used in our packaging

Suggested Emission Factor: 0.5 kg CO2e/kg
Source: Supplier certificate

Please review this request in the admin panel:
https://your-app.onrender.com/admin/ghg/materialrequest/123/change/

---
Academia Carbon - Automated Notification
```

#### User Status Update Email
```
Subject: [Academia Carbon] Material Request Update: Bamboo Fiber

Hello John,

Your material request for "Bamboo Fiber" has been approved! 
The emission factor has been added to the system.

Status: Approved - Factor Added

Admin Notes:
Added bamboo fiber with emission factor from Defra 2024 database.

You can now use this material in your calculations. 
Look for it in the emission source dropdown.

View your request:
https://your-app.onrender.com/history/

Thank you for using Academia Carbon!

---
Academia Carbon Team
```

## Troubleshooting

### Emails Not Sending

**Check 1: Email Backend**
```python
# In Django shell
from django.conf import settings
print(settings.EMAIL_BACKEND)
# Should be: django.core.mail.backends.smtp.EmailBackend (production)
```

**Check 2: SMTP Credentials**
```bash
# Test SMTP connection
python manage.py test_email
```

**Check 3: Gmail App Password**
- Make sure you're using App Password, not regular password
- App Password is 16 characters without spaces
- 2-Step Verification must be enabled

**Check 4: Firewall/Port**
- Port 587 must be open for TLS
- Port 465 for SSL (alternative)

**Check 5: Admin Emails**
```python
from django.conf import settings
print(settings.ADMIN_NOTIFICATION_EMAILS)
# Should show list of admin emails
```

### Common Errors

#### SMTPAuthenticationError
```
Solution: Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
For Gmail: Use App Password, not regular password
```

#### Connection Refused
```
Solution: Check EMAIL_HOST and EMAIL_PORT
Make sure port 587 is not blocked by firewall
```

#### No Admin Emails
```
Solution: Set ADMIN_NOTIFICATION_EMAILS in .env
Also check superuser emails in database
```

## Security Best Practices

1. **Never commit email credentials to git**
   - Use .env file
   - Add .env to .gitignore

2. **Use App Passwords for Gmail**
   - Don't use your main password
   - Generate app-specific password

3. **Use environment variables**
   - All sensitive data in .env
   - Different configs for dev/prod

4. **Limit admin emails**
   - Only send to necessary recipients
   - Use role-based emails (admin@, support@)

5. **Rate limiting (future)**
   - Prevent spam/abuse
   - Throttle notification frequency

## Monitoring

### Check Notification Logs
```bash
# In production
tail -f /var/log/django.log | grep notification

# Or check Django logs
python manage.py shell
>>> import logging
>>> logger = logging.getLogger('ghg.notifications')
```

### Admin Panel
- View all material requests: `/admin/ghg/materialrequest/`
- Filter by status
- See notification history in logs

## Future Enhancements

- [ ] Email templates with HTML styling
- [ ] Notification preferences per user
- [ ] Digest emails (daily/weekly summary)
- [ ] SMS notifications (Twilio integration)
- [ ] In-app notifications
- [ ] Webhook notifications
- [ ] Slack/Discord integration

## Files Modified

1. `carbon_tracker/settings.py` - Email configuration
2. `ghg/notifications.py` - Notification functions (NEW)
3. `ghg/views.py` - Call notifications on material request
4. `ghg/admin.py` - Call notifications on status change
5. `ghg/management/commands/test_email.py` - Test command (NEW)
6. `.env.example` - Email configuration examples

## Testing Checklist

- [x] Console backend works in development
- [x] SMTP backend works in production
- [x] Admin receives email on material request
- [x] User receives email on status change
- [x] Multiple admin emails supported
- [x] Superuser emails included automatically
- [x] Error handling (fails gracefully)
- [x] Logging for debugging
- [x] Test command works

## Status: Production Ready ✅

All notification features implemented and tested!
