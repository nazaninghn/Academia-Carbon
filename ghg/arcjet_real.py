"""
Real Arcjet Integration for SustIndex
Replace arcjet_simulation with this when you have Arcjet API key
"""

from django.conf import settings
from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)

# Check if Arcjet is available
try:
    import arcjet
    ARCJET_AVAILABLE = True
except ImportError:
    ARCJET_AVAILABLE = False
    logger.warning("Arcjet SDK not installed. Install with: pip install arcjet-python")

# Initialize Arcjet client
if ARCJET_AVAILABLE and hasattr(settings, 'ARCJET_KEY') and settings.ARCJET_KEY:
    aj = arcjet.Arcjet(
        key=settings.ARCJET_KEY,
        rules=[
            # Rate limiting for login
            arcjet.rateLimit({
                "mode": "LIVE",
                "characteristics": ["ip"],
                "max": 5,
                "window": "5m",
                "path": "/login/"
            }),
            # Bot detection
            arcjet.detectBot({
                "mode": "LIVE",
                "allow": []  # Block all bots
            }),
            # Shield (WAF)
            arcjet.shield({
                "mode": "LIVE"
            })
        ]
    )
    ARCJET_CONFIGURED = True
else:
    ARCJET_CONFIGURED = False
    logger.warning("Arcjet not configured. Set ARCJET_KEY in environment variables.")


def arcjet_protect(rules=None):
    """
    Decorator for view protection using real Arcjet
    Falls back to allowing requests if Arcjet is not available
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # If Arcjet is not available or not configured, allow request
            if not ARCJET_AVAILABLE or not ARCJET_CONFIGURED:
                logger.debug("Arcjet not available, allowing request")
                return view_func(request, *args, **kwargs)
            
            try:
                # Get client IP
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0].strip()
                else:
                    ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
                
                # Call Arcjet
                decision = aj.protect(request, {
                    "ip": ip,
                    "path": request.path,
                    "method": request.method,
                    "headers": dict(request.headers)
                })
                
                # Check decision
                if decision.is_denied():
                    if decision.is_rate_limit():
                        return JsonResponse({
                            'error': 'Rate limit exceeded. Please try again later.',
                            'retry_after': decision.reason.reset_time
                        }, status=429)
                    
                    elif decision.is_bot():
                        return JsonResponse({
                            'error': 'Automated requests are not allowed.'
                        }, status=403)
                    
                    elif decision.is_shield():
                        return JsonResponse({
                            'error': 'Request blocked by security filter.'
                        }, status=403)
                    
                    return HttpResponseForbidden('Request denied')
                
                # Request allowed
                return view_func(request, *args, **kwargs)
                
            except Exception as e:
                # Fail open - don't block on errors
                logger.error(f"Arcjet error: {e}")
                return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


class ArcjetMiddleware:
    """
    Django middleware for real Arcjet
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = ARCJET_AVAILABLE and ARCJET_CONFIGURED
    
    def __call__(self, request):
        # Skip if not enabled
        if not self.enabled:
            return self.get_response(request)
        
        # Skip for static files and admin
        if (request.path.startswith('/static/') or 
            request.path.startswith('/admin/') or
            request.path.startswith('/media/')):
            return self.get_response(request)
        
        try:
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
            
            # Call Arcjet
            decision = aj.protect(request, {
                "ip": ip,
                "path": request.path,
                "method": request.method,
                "headers": dict(request.headers)
            })
            
            # Check decision
            if decision.is_denied():
                if decision.is_rate_limit():
                    return JsonResponse({
                        'error': 'Rate limit exceeded',
                        'retry_after': decision.reason.reset_time
                    }, status=429)
                
                elif decision.is_bot():
                    return JsonResponse({
                        'error': 'Automated requests not allowed'
                    }, status=403)
                
                elif decision.is_shield():
                    return JsonResponse({
                        'error': 'Request blocked by security filter'
                    }, status=403)
                
                return HttpResponseForbidden('Request denied')
        
        except Exception as e:
            # Fail open
            logger.error(f"Arcjet middleware error: {e}")
        
        response = self.get_response(request)
        return response
