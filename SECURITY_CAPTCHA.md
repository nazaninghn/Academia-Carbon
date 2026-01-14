# Google reCAPTCHA v3 Security Implementation

## Overview

Academia Carbon uses **Google reCAPTCHA v3** to protect login and signup forms from automated bot attacks, spam, and abuse. reCAPTCHA v3 is an invisible CAPTCHA that analyzes user behavior and assigns a score (0.0 = bot, 1.0 = human) without requiring user interaction.

## Features

✅ **Invisible Protection** - No user interaction required (no "I'm not a robot" checkbox)  
✅ **Score-Based Validation** - Intelligent bot detection using behavioral analysis  
✅ **Action Verification** - Ensures tokens are used for their intended purpose  
✅ **Configurable Thresholds** - Adjust sensitivity based on security needs  
✅ **Graceful Degradation** - Can be disabled for testing/development  
✅ **Comprehensive Logging** - All verification attempts are logged for security monitoring

## How It Works

### 1. Frontend Integration

When a user submits the login or signup form:

1. JavaScript intercepts the form submission
2. Calls Google reCAPTCHA API to generate a token
3. Token is added to a hidden form field
4. Form is submitted with the token

### 2. Backend Validation

When the server receives the form:

1. Extracts the reCAPTCHA token from POST data
2. Sends token to Google's verification API
3. Google returns a score (0.0-1.0) and action name
4. Server validates:
   - Score meets threshold (default: 0.5)
   - Action matches expected value ('login' or 'signup')
5. Allows or blocks the request based on validation

### 3. Security Logging

All reCAPTCHA events are logged:
- Successful verifications
- Failed verifications
- Low scores (potential bots)
- Action mismatches
- Network errors

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Google reCAPTCHA v3 Keys
RECAPTCHA_SITE_KEY=your_site_key_here
RECAPTCHA_SECRET_KEY=your_secret_key_here

# Enable/Disable reCAPTCHA (True/False)
RECAPTCHA_ENABLED=True
```

### Django Settings

The following settings are configured in `carbon_tracker/settings.py`:

```python
# reCAPTCHA Configuration
RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY', '')
RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY', '')
RECAPTCHA_ENABLED = os.getenv('RECAPTCHA_ENABLED', 'True').lower() == 'true'
```

### Score Thresholds

Configured in `ghg/captcha.py`:

```python
RECAPTCHA_SCORE_THRESHOLD = 0.5   # Default threshold (recommended)
RECAPTCHA_STRICT_THRESHOLD = 0.7  # For sensitive operations
```

**Threshold Guidelines:**
- **0.0-0.3**: Likely bot
- **0.3-0.5**: Suspicious activity
- **0.5-0.7**: Probably human
- **0.7-1.0**: Very likely human

## Getting reCAPTCHA Keys

### 1. Register Your Site

1. Go to [Google reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin)
2. Click "+" to create a new site
3. Fill in the form:
   - **Label**: Academia Carbon
   - **reCAPTCHA type**: reCAPTCHA v3
   - **Domains**: Add your domain(s)
     - For development: `localhost`, `127.0.0.1`
     - For production: `yourdomain.com`
   - Accept terms and submit

### 2. Get Your Keys

After registration, you'll receive:
- **Site Key** (public) - Used in frontend JavaScript
- **Secret Key** (private) - Used in backend validation

### 3. Add Keys to Environment

```bash
# .env file
RECAPTCHA_SITE_KEY=6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
RECAPTCHA_SECRET_KEY=6LcYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
RECAPTCHA_ENABLED=True
```

⚠️ **IMPORTANT**: Never commit `.env` file to version control!

## Implementation Details

### Protected Views

reCAPTCHA is integrated into:

1. **Login View** (`email_login_view`)
   - Action: `login`
   - Threshold: 0.5 (default)
   - Combined with account lockout protection

2. **Signup View** (`email_signup_view`)
   - Action: `signup`
   - Threshold: 0.5 (default)
   - Prevents automated account creation

### Code Structure

```
ghg/
├── captcha.py              # reCAPTCHA validation logic
├── views.py                # Integration in login/signup views
├── tests_captcha.py        # Comprehensive test suite
└── security.py             # Security utilities (IP detection, logging)

templates/auth/
├── login.html              # Login form with reCAPTCHA
└── signup.html             # Signup form with reCAPTCHA
```

### Key Functions

#### `ReCaptchaValidator.verify_token()`
Verifies a reCAPTCHA token with Google's API.

```python
result = ReCaptchaValidator.verify_token(
    token='user_token',
    action='login',
    remote_ip='127.0.0.1'
)
# Returns: {'success': True, 'score': 0.9, 'action': 'login', ...}
```

#### `ReCaptchaValidator.is_human()`
Simple boolean check if user is human.

```python
is_human = ReCaptchaValidator.is_human(
    token='user_token',
    action='login',
    threshold=0.5
)
# Returns: True or False
```

#### `get_recaptcha_context()`
Gets reCAPTCHA context for templates.

```python
context = get_recaptcha_context()
# Returns: {'RECAPTCHA_SITE_KEY': '...', 'RECAPTCHA_ENABLED': True}
```

## Testing

### Running Tests

```bash
# Run all reCAPTCHA tests
python manage.py test ghg.tests_captcha

# Run specific test class
python manage.py test ghg.tests_captcha.ReCaptchaValidatorTests

# Run with verbose output
python manage.py test ghg.tests_captcha --verbosity=2
```

### Test Coverage

The test suite includes:
- ✅ Validator functionality (success, failure, errors)
- ✅ Score-based validation
- ✅ Action verification
- ✅ Network error handling
- ✅ Login view integration
- ✅ Signup view integration
- ✅ Template rendering
- ✅ Configuration scenarios

### Manual Testing

#### 1. Test with CAPTCHA Disabled

```bash
# .env
RECAPTCHA_ENABLED=False
```

Forms should work normally without CAPTCHA validation.

#### 2. Test with CAPTCHA Enabled

```bash
# .env
RECAPTCHA_ENABLED=True
RECAPTCHA_SITE_KEY=your_site_key
RECAPTCHA_SECRET_KEY=your_secret_key
```

1. Open login page in browser
2. Open browser DevTools (F12) → Network tab
3. Submit login form
4. Check for:
   - reCAPTCHA script loaded
   - Token generated and sent
   - Successful validation

#### 3. Test Bot Detection

Use Google's test keys to simulate different scores:

```bash
# Always passes (score 0.9)
RECAPTCHA_SITE_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_SECRET_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
```

## Security Considerations

### 1. Token Reuse Prevention

reCAPTCHA tokens are single-use and expire after 2 minutes. The system:
- Validates tokens immediately upon receipt
- Does not store tokens
- Requires new token for each submission

### 2. Action Verification

Each token is tied to a specific action ('login' or 'signup'). The system:
- Rejects tokens with mismatched actions
- Prevents token reuse across different forms
- Logs action mismatches as security events

### 3. IP-Based Validation

Client IP is sent to Google for enhanced validation:
- Helps detect distributed bot attacks
- Improves score accuracy
- Logged for security monitoring

### 4. Score Thresholds

Default threshold (0.5) balances security and usability:
- **Too low (< 0.3)**: Allows bots through
- **Too high (> 0.8)**: May block legitimate users
- **Recommended**: 0.5 for most cases, 0.7 for sensitive operations

### 5. Graceful Degradation

If reCAPTCHA service is unavailable:
- Network errors are caught and logged
- Users see friendly error message
- System remains functional (doesn't block all access)

### 6. Privacy Considerations

reCAPTCHA v3 collects user data for analysis:
- User behavior patterns
- Browser fingerprints
- IP addresses

Ensure your privacy policy discloses this data collection.

## Monitoring and Logging

### Security Logs

All reCAPTCHA events are logged to `logs/security.log`:

```
[INFO] reCAPTCHA verified: action=login, score=0.9, hostname=example.com
[WARNING] reCAPTCHA score too low: 0.3 < 0.5 (action=login, ip=192.168.1.1)
[WARNING] reCAPTCHA action mismatch: expected=login, got=signup
[ERROR] reCAPTCHA verification request failed: Network timeout
```

### Monitoring Recommendations

1. **Track Failed Verifications**
   - High failure rate may indicate bot attacks
   - Or misconfigured keys

2. **Monitor Low Scores**
   - Frequent low scores from same IP = bot
   - Adjust threshold if too many false positives

3. **Check Action Mismatches**
   - May indicate token manipulation attempts
   - Or frontend/backend version mismatch

4. **Alert on Network Errors**
   - reCAPTCHA service outage
   - Network connectivity issues

## Troubleshooting

### Issue: "Security verification failed" on every login

**Possible Causes:**
1. Invalid or missing reCAPTCHA keys
2. Domain not registered in reCAPTCHA console
3. Network connectivity issues
4. JavaScript errors preventing token generation

**Solutions:**
1. Verify keys in `.env` file
2. Check domain registration in reCAPTCHA console
3. Check browser console for JavaScript errors
4. Test with `RECAPTCHA_ENABLED=False` to isolate issue

### Issue: Legitimate users being blocked

**Possible Causes:**
1. Threshold too high
2. Users behind VPN/proxy
3. Browser privacy extensions blocking reCAPTCHA

**Solutions:**
1. Lower threshold to 0.4 or 0.3
2. Add fallback authentication method
3. Provide clear error messages to users

### Issue: reCAPTCHA script not loading

**Possible Causes:**
1. `RECAPTCHA_ENABLED=False` in settings
2. Missing site key
3. Content Security Policy blocking script
4. Ad blockers

**Solutions:**
1. Set `RECAPTCHA_ENABLED=True`
2. Verify `RECAPTCHA_SITE_KEY` is set
3. Update CSP headers to allow Google domains
4. Test in incognito mode without extensions

### Issue: High bot traffic still getting through

**Possible Causes:**
1. Threshold too low
2. Sophisticated bots with high scores
3. Token manipulation

**Solutions:**
1. Increase threshold to 0.7
2. Combine with rate limiting (already implemented)
3. Add additional security measures (account lockout, email verification)

## Best Practices

### 1. Development vs Production

**Development:**
```bash
RECAPTCHA_ENABLED=False  # Easier testing
```

**Production:**
```bash
RECAPTCHA_ENABLED=True
RECAPTCHA_SITE_KEY=production_site_key
RECAPTCHA_SECRET_KEY=production_secret_key
```

### 2. Key Management

- ✅ Store keys in environment variables
- ✅ Use different keys for dev/staging/production
- ✅ Rotate keys periodically
- ❌ Never commit keys to version control
- ❌ Never expose secret key in frontend

### 3. User Experience

- ✅ Use invisible reCAPTCHA v3 (no user interaction)
- ✅ Provide clear error messages
- ✅ Don't mention "bot detection" to users
- ✅ Combine with other security measures
- ❌ Don't rely solely on reCAPTCHA

### 4. Monitoring

- ✅ Monitor verification success rates
- ✅ Track score distributions
- ✅ Alert on unusual patterns
- ✅ Review logs regularly
- ❌ Don't ignore security warnings

## Integration with Other Security Features

reCAPTCHA works alongside other security measures:

### 1. Account Lockout
- reCAPTCHA validates first
- Account lockout checks second
- Both must pass for login

### 2. Rate Limiting
- reCAPTCHA prevents automated attacks
- Rate limiting prevents brute force
- Complementary protections

### 3. Email Uniqueness
- reCAPTCHA prevents bot signups
- Email uniqueness prevents duplicates
- Both enforce data integrity

## Performance Impact

### Frontend
- **Script Size**: ~50KB (cached by Google CDN)
- **Load Time**: <100ms (async loading)
- **User Impact**: Minimal (invisible)

### Backend
- **Verification Time**: 100-300ms per request
- **Network Overhead**: Single HTTPS request to Google
- **CPU Impact**: Negligible (JSON parsing only)

### Optimization Tips
1. Load reCAPTCHA script asynchronously
2. Cache verification results (not implemented - tokens are single-use)
3. Use CDN for static assets
4. Monitor Google API response times

## Compliance and Privacy

### GDPR Compliance

reCAPTCHA v3 processes personal data:
- IP addresses
- Browser fingerprints
- User behavior patterns

**Requirements:**
1. Update privacy policy to disclose reCAPTCHA usage
2. Provide opt-out mechanism (if required by jurisdiction)
3. Include Google's privacy policy link
4. Obtain user consent (if required)

### Data Processing Agreement

Google provides a Data Processing Amendment for reCAPTCHA:
- [Google Cloud Data Processing Amendment](https://cloud.google.com/terms/data-processing-addendum)

## Support and Resources

### Official Documentation
- [reCAPTCHA v3 Documentation](https://developers.google.com/recaptcha/docs/v3)
- [reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin)
- [reCAPTCHA FAQ](https://developers.google.com/recaptcha/docs/faq)

### Academia Carbon Resources
- `ghg/captcha.py` - Implementation code
- `ghg/tests_captcha.py` - Test suite
- `SECURITY_ACCOUNT_LOCKOUT.md` - Account lockout documentation
- `SECURITY_EMAIL_UNIQUE.md` - Email uniqueness documentation

### Getting Help

1. Check logs: `logs/security.log`
2. Run tests: `python manage.py test ghg.tests_captcha`
3. Review this documentation
4. Check Google reCAPTCHA status: [status.cloud.google.com](https://status.cloud.google.com)

## Changelog

### Version 1.0 (2024-01-14)
- ✅ Initial implementation of reCAPTCHA v3
- ✅ Integration with login and signup views
- ✅ Comprehensive test suite
- ✅ Security logging
- ✅ Configuration management
- ✅ Documentation

---

**Last Updated**: January 14, 2024  
**Maintained By**: Academia Carbon Security Team  
**Status**: ✅ Production Ready
