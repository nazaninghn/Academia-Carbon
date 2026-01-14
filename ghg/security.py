"""
Security utilities for Academia Carbon
Includes account lockout, failed login tracking, and security monitoring
"""

import logging
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger('ghg.security')

# Security Configuration
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 30  # minutes
FAILED_LOGIN_CACHE_PREFIX = 'failed_login_'
LOCKOUT_CACHE_PREFIX = 'account_locked_'


class AccountLockout:
    """Handle account lockout after failed login attempts"""
    
    @staticmethod
    def get_failed_attempts(identifier):
        """
        Get number of failed login attempts for an identifier (email or IP)
        
        Args:
            identifier: Email address or IP address
            
        Returns:
            int: Number of failed attempts
        """
        cache_key = f"{FAILED_LOGIN_CACHE_PREFIX}{identifier}"
        return cache.get(cache_key, 0)
    
    @staticmethod
    def increment_failed_attempts(identifier):
        """
        Increment failed login attempts counter
        
        Args:
            identifier: Email address or IP address
            
        Returns:
            int: New number of failed attempts
        """
        cache_key = f"{FAILED_LOGIN_CACHE_PREFIX}{identifier}"
        attempts = cache.get(cache_key, 0) + 1
        
        # Store for 30 minutes
        cache.set(cache_key, attempts, LOCKOUT_DURATION * 60)
        
        logger.warning(
            f"Failed login attempt #{attempts} for {identifier}"
        )
        
        # Lock account if max attempts reached
        if attempts >= MAX_LOGIN_ATTEMPTS:
            AccountLockout.lock_account(identifier)
        
        return attempts
    
    @staticmethod
    def reset_failed_attempts(identifier):
        """
        Reset failed login attempts counter (after successful login)
        
        Args:
            identifier: Email address or IP address
        """
        cache_key = f"{FAILED_LOGIN_CACHE_PREFIX}{identifier}"
        cache.delete(cache_key)
        
        logger.info(f"Reset failed attempts for {identifier}")
    
    @staticmethod
    def is_locked(identifier):
        """
        Check if account/IP is locked
        
        Args:
            identifier: Email address or IP address
            
        Returns:
            bool: True if locked, False otherwise
        """
        cache_key = f"{LOCKOUT_CACHE_PREFIX}{identifier}"
        return cache.get(cache_key, False)
    
    @staticmethod
    def lock_account(identifier):
        """
        Lock account/IP for specified duration
        
        Args:
            identifier: Email address or IP address
        """
        cache_key = f"{LOCKOUT_CACHE_PREFIX}{identifier}"
        cache.set(cache_key, True, LOCKOUT_DURATION * 60)
        
        logger.error(
            f"🔒 ACCOUNT LOCKED: {identifier} - "
            f"Too many failed login attempts. "
            f"Locked for {LOCKOUT_DURATION} minutes."
        )
    
    @staticmethod
    def unlock_account(identifier):
        """
        Manually unlock account/IP
        
        Args:
            identifier: Email address or IP address
        """
        cache_key = f"{LOCKOUT_CACHE_PREFIX}{identifier}"
        cache.delete(cache_key)
        AccountLockout.reset_failed_attempts(identifier)
        
        logger.info(f"🔓 Account unlocked: {identifier}")
    
    @staticmethod
    def get_lockout_time_remaining(identifier):
        """
        Get remaining lockout time in seconds
        
        Args:
            identifier: Email address or IP address
            
        Returns:
            int: Remaining seconds, or 0 if not locked
        """
        cache_key = f"{LOCKOUT_CACHE_PREFIX}{identifier}"
        ttl = cache.ttl(cache_key)
        return max(0, ttl) if ttl else 0
    
    @staticmethod
    def get_attempts_remaining(identifier):
        """
        Get number of attempts remaining before lockout
        
        Args:
            identifier: Email address or IP address
            
        Returns:
            int: Attempts remaining
        """
        failed = AccountLockout.get_failed_attempts(identifier)
        return max(0, MAX_LOGIN_ATTEMPTS - failed)


def get_client_ip(request):
    """
    Get client IP address from request
    
    Args:
        request: Django request object
        
    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def check_suspicious_activity(request):
    """
    Check for suspicious activity patterns
    
    Args:
        request: Django request object
        
    Returns:
        bool: True if suspicious, False otherwise
    """
    # Check for suspicious user agents
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    suspicious_agents = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget']
    
    for agent in suspicious_agents:
        if agent in user_agent:
            logger.warning(
                f"Suspicious user agent detected: {user_agent} "
                f"from IP: {get_client_ip(request)}"
            )
            return True
    
    return False


def log_security_event(event_type, identifier, details=''):
    """
    Log security events for monitoring
    
    Args:
        event_type: Type of security event (login_failed, account_locked, etc.)
        identifier: Email or IP address
        details: Additional details
    """
    logger.info(
        f"SECURITY EVENT: {event_type} | "
        f"Identifier: {identifier} | "
        f"Details: {details}"
    )
