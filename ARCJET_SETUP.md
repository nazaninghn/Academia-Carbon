# 🛡️ Arcjet Setup Guide

## Current Status

You are currently using **Arcjet Simulation** (`ghg/arcjet_simulation.py`), which mimics Arcjet functionality using Django's built-in tools.

## Switching to Real Arcjet

### Step 1: Sign Up for Arcjet

1. Go to https://arcjet.com
2. Create an account
3. Create a new project
4. Copy your API key

### Step 2: Install Arcjet SDK

```bash
pip install arcjet-python
```

Add to `requirements.txt`:
```
arcjet-python>=1.0.0
```

### Step 3: Configure Environment Variables

**On Render:**
1. Go to your service dashboard
2. Click "Environment"
3. Add these variables:
   ```
   ARCJET_KEY=ajkey_your_actual_key_here
   ARCJET_MODE=LIVE
   ARCJET_ENABLED=True
   ```

**Locally (.env):**
```env
ARCJET_KEY=ajkey_your_actual_key_here
ARCJET_MODE=DRY_RUN  # Use DRY_RUN for testing
ARCJET_ENABLED=True
```

### Step 4: Update Middleware

In `carbon_tracker/settings.py`, replace:

```python
# OLD
'ghg.arcjet_simulation.ArcjetSimulatorMiddleware',

# NEW
'ghg.arcjet_real.ArcjetMiddleware',
```

### Step 5: Update Imports

In your views (`ghg/views.py`), replace:

```python
# OLD
from .arcjet_simulation import arcjet_protect

# NEW
from .arcjet_real import arcjet_protect
```

### Step 6: Deploy

```bash
git add .
git commit -m "Switch to real Arcjet"
git push origin main
```

---

## Arcjet Features

### 1. Rate Limiting
Protects against brute force attacks:
- Login: 5 attempts per 5 minutes
- Signup: 3 attempts per hour
- API: 100 requests per minute

### 2. Bot Detection
Blocks automated requests:
- Suspicious user agents
- Missing headers
- Behavioral patterns

### 3. Shield (WAF)
Web Application Firewall:
- SQL injection protection
- XSS attack prevention
- Path traversal blocking

---

## Testing Arcjet

### Test Rate Limiting

```bash
# Make multiple rapid requests
for i in {1..10}; do
  curl -X POST http://localhost:8000/en/login/ \
    -d "username=test@example.com&password=wrong"
done
```

### Test Bot Detection

```bash
# Request with bot user agent
curl http://localhost:8000/ \
  -H "User-Agent: bot/1.0"
```

### Check Arcjet Dashboard

1. Go to https://app.arcjet.com
2. View your project
3. See real-time security events
4. Analyze blocked requests

---

## Modes

### DRY_RUN
- Logs decisions but doesn't block
- Good for testing

### LIVE
- Actively blocks malicious requests
- Use in production

---

## Comparison: Simulation vs Real

| Feature | Simulation | Real Arcjet |
|---------|-----------|-------------|
| Rate Limiting | ✅ Basic | ✅ Advanced |
| Bot Detection | ✅ Simple | ✅ ML-powered |
| WAF | ✅ Basic | ✅ Enterprise |
| Dashboard | ❌ No | ✅ Yes |
| Analytics | ❌ No | ✅ Yes |
| Cost | ✅ Free | 💰 Paid |

---

## Pricing

Check https://arcjet.com/pricing for current pricing.

Free tier typically includes:
- 100,000 requests/month
- Basic rate limiting
- Bot detection
- Email support

---

## Troubleshooting

### Arcjet not working?

1. Check API key is correct
2. Verify `arcjet-python` is installed
3. Check logs: `tail -f logs/security.log`
4. Test with DRY_RUN mode first

### Too many blocks?

1. Adjust rate limits in `arcjet_real.py`
2. Whitelist your IP
3. Use DRY_RUN to test

### Need help?

- Arcjet Docs: https://docs.arcjet.com
- Arcjet Support: support@arcjet.com
- GitHub Issues: https://github.com/nazaninghn/Academia-Carbon/issues

---

## Keeping Simulation

If you want to keep using the simulation:

1. Don't change anything
2. Current setup works fine
3. No cost
4. Good for development

The simulation provides:
- ✅ Rate limiting
- ✅ Basic bot detection
- ✅ Simple WAF
- ✅ Account lockout
- ✅ Security logging

---

**Current Setup:** Arcjet Simulation (Free, works well)

**Upgrade to Real Arcjet when:**
- You need advanced bot detection
- You want analytics dashboard
- You need enterprise-grade WAF
- You have budget for security tools
