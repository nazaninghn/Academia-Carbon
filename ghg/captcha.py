"""
Google reCAPTCHA v3 Integration for Academia Carbon
Provides invisible CAPTCHA protection for forms
"""

import requests
import logging
from django.conf import settings

logger = logging.getLogger('ghg.security')

# reCAPTCHA Configuration
RECAPTCHA_SITE_KEY = getattr(settings, 'RECAPTCHA_SITE_KEY', '')
RECAPTCHA_SECRET_KEY = getattr(settings, 'RECAPTCHA_SECRET_KEY', '')
RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
RECAPTCHA_ENABLED = getattr(settings, 'RECAPTCHA_ENABLED', True)

# Score thresholds (0.0 = bot, 1.0 = human)
RECAPTCHA_SCORE_THRESHOLD = 0.5  # Default threshold
RECAPTCHA_STRICT_THRESHOLD = 0.7  # For sensitive operations


class ReCaptchaValidator:
    """Validate Google reCAPTCHA v3 responses"""
    
    @staticmethod
    def verify_token(token, action='submit', remote_ip=None):
        """
        Verify reCAPTCHA token with Google
        
        Args:
            token: reCAPTCHA token from frontend
            action: Expected action name (e.g., 'login', 'signup')
            remote_ip: Client IP address (optional)
            
        Returns:
            dict: {
                'success': bool,
                'score': float (0.0-1.0),
                'action': str,
                'challenge_ts': str,
                'hostname': str,
                'error_codes': list
            }
        """
        # Skip verification if CAPTCHA is disabled (for testing)
        if not RECAPTCHA_ENABLED:
            logger.warning("reCAPTCHA is disabled - skipping verification")
            return {
                'success': True,
                'score': 1.0,
                'action': action,
                'bypass': True
            }
        
        # Check if keys are configured
        if not RECAPTCHA_SECRET_KEY:
            logger.error("reCAPTCHA SECRET_KEY not configured")
            # If disabled, allow through; otherwise block
            if not RECAPTCHA_ENABLED:
                return {
                    'success': True,
                    'score': 1.0,
                    'action': action,
                    'bypass': True
                }
            return {
                'success': False,
                'score': 0.0,
                'error_codes': ['missing-secret-key']
            }
        
        if not token:
            logger.warning("No reCAPTCHA token provided")
            return {
                'success': False,
                'score': 0.0,
                'error_codes': ['missing-input-response']
            }
        
        # Prepare verification request
        payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': token,
        }
        
        if remote_ip:
            payload['remoteip'] = remote_ip
        
        try:
            # Send verification request to Google
            response = requests.post(
                RECAPTCHA_VERIFY_URL,
                data=payload,
                timeout=5
            )
            response.raise_for_status()
            result = response.json()
            
            # Log the verification
            if result.get('success'):
                logger.info(
                    f"reCAPTCHA verified: action={result.get('action')}, "
                    f"score={result.get('score')}, hostname={result.get('hostname')}"
                )
            else:
                logger.warning(
                    f"reCAPTCHA verification failed: "
                    f"errors={result.get('error-codes')}"
                )
            
            return result
            
        except requests.RequestException as e:
            logger.error(f"reCAPTCHA verification request failed: {str(e)}")
            return {
                'success': False,
                'score': 0.0,
                'error_codes': ['network-error']
            }
        except Exception as e:
            logger.error(f"reCAPTCHA verification error: {str(e)}")
            return {
                'success': False,
                'score': 0.0,
                'error_codes': ['unknown-error']
            }
    
    @staticmethod
    def is_human(token, action='submit', remote_ip=None, threshold=None):
        """
        Simple check if user is human based on reCAPTCHA score
        
        Args:
            token: reCAPTCHA token
            action: Expected action name
            remote_ip: Client IP address
            threshold: Custom score threshold (default: 0.5)
            
        Returns:
            bool: True if human, False if bot
        """
        if threshold is None:
            threshold = RECAPTCHA_SCORE_THRESHOLD
        
        result = ReCaptchaValidator.verify_token(token, action, remote_ip)
        
        if not result.get('success'):
            # If verification failed, treat as bot
            return False
        
        score = result.get('score', 0.0)
        
        # Check if action matches
        expected_action = result.get('action', '')
        if expected_action != action:
            logger.warning(
                f"reCAPTCHA action mismatch: expected={action}, got={expected_action}"
            )
            return False
        
        # Check score threshold
        is_human = score >= threshold
        
        if not is_human:
            logger.warning(
                f"reCAPTCHA score too low: {score} < {threshold} "
                f"(action={action}, ip={remote_ip})"
            )
        
        return is_human
    
    @staticmethod
    def get_score(token, action='submit', remote_ip=None):
        """
        Get reCAPTCHA score only
        
        Args:
            token: reCAPTCHA token
            action: Expected action name
            remote_ip: Client IP address
            
        Returns:
            float: Score between 0.0 (bot) and 1.0 (human)
        """
        result = ReCaptchaValidator.verify_token(token, action, remote_ip)
        return result.get('score', 0.0)


def require_recaptcha(action='submit', threshold=None):
    """
    Decorator to require reCAPTCHA verification for views
    
    Usage:
        @require_recaptcha(action='login', threshold=0.7)
        def login_view(request):
            ...
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if request.method == 'POST':
                token = request.POST.get('g-recaptcha-response') or \
                        request.POST.get('recaptcha_token')
                
                from .security import get_client_ip
                remote_ip = get_client_ip(request)
                
                if not ReCaptchaValidator.is_human(token, action, remote_ip, threshold):
                    from django.contrib import messages
                    messages.error(
                        request,
                        '🤖 reCAPTCHA verification failed. Please try again.'
                    )
                    # Return to the same page with error
                    return view_func(request, *args, **kwargs)
            
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    return decorator


def get_recaptcha_context():
    """
    Get reCAPTCHA context for templates
    
    Returns:
        dict: Context with site key and enabled status
    """
    return {
        'RECAPTCHA_SITE_KEY': RECAPTCHA_SITE_KEY,
        'RECAPTCHA_ENABLED': RECAPTCHA_ENABLED and bool(RECAPTCHA_SITE_KEY) and bool(RECAPTCHA_SECRET_KEY),
    }
