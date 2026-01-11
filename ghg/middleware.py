"""
Security middleware for Academia Carbon
"""

import logging
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
import time

logger = logging.getLogger('ghg.security')

class SecurityLoggingMiddleware(MiddlewareMixin):
    """Log security-related events"""
    
    def process_request(self, request):
        # Log suspicious requests
        suspicious_patterns = [
            'admin', 'wp-admin', 'phpmyadmin', '.env', 'config',
            'backup', 'sql', 'database', 'shell', 'cmd'
        ]
        
        path = request.path.lower()
        for pattern in suspicious_patterns:
            if pattern in path and not path.startswith('/admin/'):
                logger.warning(
                    f"Suspicious request: {request.method} {request.path} "
                    f"from {self.get_client_ip(request)} "
                    f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
                )
                break
        
        return None
    
    def process_response(self, request, response):
        # Log failed login attempts
        if (request.path.endswith('/login/') and 
            response.status_code == 200 and 
            request.method == 'POST'):
            
            # Check if login failed (form errors in response)
            if hasattr(response, 'context_data') and response.context_data:
                form = response.context_data.get('form')
                if form and form.errors:
                    logger.warning(
                        f"Failed login attempt from {self.get_client_ip(request)} "
                        f"for user: {request.POST.get('email', 'Unknown')}"
                    )
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RateLimitMiddleware(MiddlewareMixin):
    """Simple rate limiting middleware"""
    
    def process_request(self, request):
        # Skip rate limiting for static files
        if request.path.startswith('/static/'):
            return None
        
        client_ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{client_ip}"
        
        # Get current request count
        requests = cache.get(cache_key, 0)
        
        # Rate limit: 100 requests per minute
        if requests >= 100:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return HttpResponseForbidden("Rate limit exceeded. Please try again later.")
        
        # Increment counter
        cache.set(cache_key, requests + 1, 60)  # 60 seconds
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add additional security headers"""
    
    def process_response(self, request, response):
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Remove server information
        if 'Server' in response:
            del response['Server']
        
        return response