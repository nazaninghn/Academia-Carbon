# Arcjet Security Integration for Academia Carbon

## Overview
Arcjet provides application-layer security for Django applications with bot detection, rate limiting, email validation, and attack protection.

## Installation

### Step 1: Install Arcjet Python SDK
```bash
# When available (currently in beta)
pip install arcjet

# Or from source if needed
pip install git+https://github.com/arcjet/arcjet-python.git
```

### Step 2: Get API Key
1. Sign up at [https://app.arcjet.com](https://app.arcjet.com)
2. Create a new site
3. Copy your API key

### Step 3: Environment Variables
Add to your `.env` file:
```bash
ARCJET_KEY=your_api_key_here
```

## Implementation

### 1. Basic Configuration
Create `ghg/arcjet_config.py`:

```python
import os
from arcjet import Arcjet, shield, rate_limit, detect_bot, Mode

# Initialize Arcjet client
arcjet = Arcjet(
    key=os.getenv('ARCJET_KEY'),
    rules=[
        # Shield WAF - protects against common attacks
        shield(mode=Mode.LIVE),
        
        # Rate limiting - 100 requests per minute per IP
        rate_limit(
            max=100,
            window="1m",
            mode=Mode.LIVE
        ),
        
        # Bot detection - block automated clients
        detect_bot(
            mode=Mode.LIVE,
            allow=[]  # Allow no bots by default
        )
    ]
)
```

### 2. Django Middleware
Create `ghg/middleware/arcjet_middleware.py`:

```python
import asyncio
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from ..arcjet_config import arcjet

class ArcjetMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip for static files and admin
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return None
            
        # Convert Django request to Arcjet format
        arcjet_request = {
            'ip': self.get_client_ip(request),
            'method': request.method,
            'url': request.build_absolute_uri(),
            'headers': dict(request.headers),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
        
        # Make decision (sync version for Django)
        try:
            decision = arcjet.protect(arcjet_request)
            
            if decision.is_denied():
                if decision.reason.is_rate_limit():
                    return JsonResponse({
                        'error': 'Rate limit exceeded',
                        'retry_after': decision.reason.reset_time
                    }, status=429)
                    
                elif decision.reason.is_bot():
                    return JsonResponse({
                        'error': 'Automated requests not allowed'
                    }, status=403)
                    
                elif decision.reason.is_shield():
                    return JsonResponse({
                        'error': 'Request blocked by security filter'
                    }, status=403)
                    
                # Generic forbidden response
                return HttpResponseForbidden('Request denied')
                
        except Exception as e:
            # Fail open - don't block requests if Arcjet fails
            print(f"Arcjet error: {e}")
            
        return None
    
    def get_client_ip(self, request):
        """Get real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

### 3. View-Level Protection
For specific views that need extra protection:

```python
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .arcjet_config import arcjet

def arcjet_protect(rules=None):
    """Decorator for view-level Arcjet protection"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Create custom Arcjet instance with specific rules
            if rules:
                custom_arcjet = Arcjet(
                    key=os.getenv('ARCJET_KEY'),
                    rules=rules
                )
            else:
                custom_arcjet = arcjet
                
            arcjet_request = {
                'ip': get_client_ip(request),
                'method': request.method,
                'url': request.build_absolute_uri(),
                'headers': dict(request.headers),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            }
            
            decision = custom_arcjet.protect(arcjet_request)
            
            if decision.is_denied():
                return JsonResponse({
                    'error': 'Request denied',
                    'reason': str(decision.reason)
                }, status=403)
                
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Example usage in views.py
@arcjet_protect([
    rate_limit(max=5, window="1m"),  # Stricter rate limit for login
    detect_bot(mode=Mode.LIVE)
])
def email_login_view(request):
    # Your login logic here
    pass
```

### 4. Settings Configuration
Add to `carbon_tracker/settings.py`:

```python
# Add Arcjet middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'ghg.middleware.arcjet_middleware.ArcjetMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest of middleware
]

# Arcjet settings
ARCJET_KEY = os.getenv('ARCJET_KEY')
ARCJET_MODE = 'LIVE'  # or 'DRY_RUN' for testing
```

## Advanced Features

### 1. Email Validation
```python
from arcjet import validate_email

@arcjet_protect([validate_email(mode=Mode.LIVE)])
def signup_view(request):
    email = request.POST.get('email')
    # Email will be validated by Arcjet
    pass
```

### 2. Custom Rate Limits per User Type
```python
def get_rate_limit_for_user(user):
    if user.is_premium:
        return rate_limit(max=1000, window="1h")
    else:
        return rate_limit(max=100, window="1h")

@arcjet_protect()
def api_endpoint(request):
    # Dynamic rate limiting based on user
    pass
```

### 3. Signup Protection
```python
from arcjet import protect_signup

@arcjet_protect([
    protect_signup(
        email=True,
        bots=True,
        rate_limit=rate_limit(max=5, window="1h")
    )
])
def signup_view(request):
    # Protected signup form
    pass
```

## Integration with Existing Security

### Combine with Current Rate Limiting
```python
# Keep your existing django-ratelimit as backup
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='30/m', method='POST')  # Existing
@arcjet_protect([rate_limit(max=20, window="1m")])  # Arcjet (stricter)
def sensitive_view(request):
    # Double protection
    pass
```

### Enhance CAPTCHA Protection
```python
@arcjet_protect([
    detect_bot(mode=Mode.LIVE),
    rate_limit(max=3, window="5m")  # Very strict for CAPTCHA
])
def captcha_view(request):
    # Your existing CAPTCHA logic + Arcjet bot detection
    pass
```

## Monitoring & Analytics

### Dashboard
- View real-time security events at [https://app.arcjet.com](https://app.arcjet.com)
- See blocked requests, rate limits, bot detections
- Configure alerts for security events

### Logging
```python
import logging

logger = logging.getLogger('arcjet')

def process_request(self, request):
    decision = arcjet.protect(arcjet_request)
    
    if decision.is_denied():
        logger.warning(f"Arcjet blocked request: {decision.reason}")
    
    return None
```

## Testing

### Development Mode
```python
# In development, use DRY_RUN mode
arcjet = Arcjet(
    key=os.getenv('ARCJET_KEY'),
    rules=[
        shield(mode=Mode.DRY_RUN),  # Log only, don't block
        rate_limit(max=100, window="1m", mode=Mode.DRY_RUN)
    ]
)
```

### Unit Tests
```python
from unittest.mock import patch
from django.test import TestCase

class ArcjetTestCase(TestCase):
    @patch('ghg.arcjet_config.arcjet.protect')
    def test_rate_limit_protection(self, mock_protect):
        mock_protect.return_value.is_denied.return_value = True
        response = self.client.post('/api/endpoint/')
        self.assertEqual(response.status_code, 429)
```

## Benefits for Academia Carbon

1. **Enhanced Bot Protection**: Better than basic user-agent checking
2. **Intelligent Rate Limiting**: Context-aware, no Redis needed
3. **Attack Prevention**: WAF protection against SQL injection, XSS
4. **Easy Integration**: Works alongside existing security
5. **Real-time Analytics**: Dashboard for security insights
6. **Low Latency**: <1ms decision time
7. **Fail-safe**: Fails open if service unavailable

## Migration Strategy

1. **Phase 1**: Install in DRY_RUN mode, monitor logs
2. **Phase 2**: Enable LIVE mode for bot detection only
3. **Phase 3**: Add rate limiting (less strict than current)
4. **Phase 4**: Enable full WAF protection
5. **Phase 5**: Fine-tune rules based on analytics

## Cost Considerations

- **Free Tier**: Limited requests per month
- **Paid Plans**: Scale with usage
- **ROI**: Reduced server load, better security, less manual monitoring

## Next Steps

1. Sign up for Arcjet account
2. Install SDK when available
3. Start with DRY_RUN mode
4. Gradually enable features
5. Monitor dashboard and adjust rules