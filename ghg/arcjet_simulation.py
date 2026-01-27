"""
Arcjet-style Security Simulation
A lightweight implementation that mimics Arcjet's functionality
using existing Django tools until the real SDK is available
"""

import time
import hashlib
from django.core.cache import cache
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from functools import wraps
import re
import logging

logger = logging.getLogger(__name__)

class SecurityDecision:
    def __init__(self, allowed=True, reason=None, details=None):
        self.allowed = allowed
        self.reason = reason
        self.details = details or {}
    
    def is_denied(self):
        return not self.allowed
    
    def is_rate_limit(self):
        return self.reason == 'rate_limit'
    
    def is_bot(self):
        return self.reason == 'bot_detected'
    
    def is_shield(self):
        return self.reason == 'shield_block'

class ArcjetSimulator:
    """Simulates Arcjet functionality using Django's built-in tools"""
    
    # Known bot user agents
    BOT_PATTERNS = [
        r'bot', r'crawler', r'spider', r'scraper', r'curl', r'wget',
        r'python-requests', r'http', r'scanner', r'test', r'monitor',
        r'check', r'probe', r'fetch', r'download', r'automation'
    ]
    
    # Suspicious patterns (basic WAF)
    ATTACK_PATTERNS = [
        r'<script', r'javascript:', r'onload=', r'onerror=',
        r'union.*select', r'drop.*table', r'insert.*into',
        r'\.\./', r'etc/passwd', r'cmd.exe', r'powershell',
        r'eval\(', r'exec\(', r'system\(', r'shell_exec'
    ]
    
    def __init__(self, rules=None):
        self.rules = rules or []
    
    def protect(self, request):
        """Main protection method"""
        try:
            # Get client info
            ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            
            # Check rate limits
            if self.is_rate_limited(ip, request.path):
                return SecurityDecision(
                    allowed=False,
                    reason='rate_limit',
                    details={'ip': ip, 'reset_time': 60}
                )
            
            # Check for bots
            if self.is_bot(user_agent, request):
                return SecurityDecision(
                    allowed=False,
                    reason='bot_detected',
                    details={'user_agent': user_agent}
                )
            
            # Check for attacks (basic WAF)
            if self.is_attack(request):
                return SecurityDecision(
                    allowed=False,
                    reason='shield_block',
                    details={'path': request.path}
                )
            
            # Log successful request
            self.log_request(ip, user_agent, request.path, 'allowed')
            
            return SecurityDecision(allowed=True)
            
        except Exception as e:
            logger.error(f"ArcjetSimulator error: {e}")
            # Fail open - don't block on errors
            return SecurityDecision(allowed=True)
    
    def get_client_ip(self, request):
        """Get real client IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
    
    def is_rate_limited(self, ip, path):
        """Check if IP is rate limited"""
        # Different limits for different endpoints - more relaxed for development
        limits = {
            '/login/': {'max': 20, 'window': 300},  # 20 per 5 minutes (was 5)
            '/signup/': {'max': 10, 'window': 3600},  # 10 per hour (was 3)
            '/api/': {'max': 200, 'window': 60},  # 200 per minute (was 100)
            'default': {'max': 500, 'window': 60}  # 500 per minute (was 200)
        }
        
        # Find matching limit
        limit_config = limits.get('default')
        for pattern, config in limits.items():
            if pattern != 'default' and pattern in path:
                limit_config = config
                break
        
        # Create cache key
        cache_key = f"arcjet_rate:{hashlib.md5(f'{ip}:{path}'.encode()).hexdigest()}"
        
        # Get current count
        current_count = cache.get(cache_key, 0)
        
        if current_count >= limit_config['max']:
            return True
        
        # Increment counter
        cache.set(cache_key, current_count + 1, limit_config['window'])
        return False
    
    def is_bot(self, user_agent, request):
        """Detect if request is from a bot"""
        if not user_agent:
            return True  # No user agent = suspicious
        
        # Check against known bot patterns
        for pattern in self.BOT_PATTERNS:
            if re.search(pattern, user_agent, re.IGNORECASE):
                return True
        
        # Check for missing common headers
        if not request.META.get('HTTP_ACCEPT'):
            return True
        
        # Check for suspicious behavior
        if len(user_agent) < 10 or len(user_agent) > 500:
            return True
        
        return False
    
    def is_attack(self, request):
        """Basic WAF - detect common attacks"""
        # Check URL path
        path = request.path.lower()
        for pattern in self.ATTACK_PATTERNS:
            if re.search(pattern, path, re.IGNORECASE):
                return True
        
        # Check query parameters
        query_string = request.META.get('QUERY_STRING', '').lower()
        for pattern in self.ATTACK_PATTERNS:
            if re.search(pattern, query_string, re.IGNORECASE):
                return True
        
        # Check POST data (if available)
        if hasattr(request, 'body') and request.body:
            try:
                body = request.body.decode('utf-8', errors='ignore').lower()
                for pattern in self.ATTACK_PATTERNS:
                    if re.search(pattern, body, re.IGNORECASE):
                        return True
            except:
                pass
        
        return False
    
    def log_request(self, ip, user_agent, path, status):
        """Log security events"""
        logger.info(f"ArcjetSim: {ip} | {user_agent[:50]} | {path} | {status}")

# Global instance
arcjet_sim = ArcjetSimulator()

def arcjet_protect(rules=None):
    """Decorator for view protection"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            decision = arcjet_sim.protect(request)
            
            if decision.is_denied():
                if decision.is_rate_limit():
                    return JsonResponse({
                        'error': 'Rate limit exceeded. Please try again later.',
                        'retry_after': decision.details.get('reset_time', 60)
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
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Middleware class
class ArcjetSimulatorMiddleware:
    """Django middleware for Arcjet simulation"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip for static files and admin
        if (request.path.startswith('/static/') or 
            request.path.startswith('/admin/') or
            request.path.startswith('/media/')):
            return self.get_response(request)
        
        # Check with Arcjet simulator
        decision = arcjet_sim.protect(request)
        
        if decision.is_denied():
            if decision.is_rate_limit():
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'retry_after': decision.details.get('reset_time', 60)
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
        
        response = self.get_response(request)
        return response