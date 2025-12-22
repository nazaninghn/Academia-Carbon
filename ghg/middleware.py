"""
Custom middleware for Academia Carbon
"""
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware:
    """
    Middleware to handle errors gracefully in production
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Handle exceptions and provide user-friendly error pages
        """
        if not settings.DEBUG:
            logger.error(f"Error in {request.path}: {str(exception)}", exc_info=True)
            
            # For API requests, return JSON error
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'error': 'Internal server error',
                    'message': 'An error occurred while processing your request.'
                }, status=500)
            
            # For regular requests, return error page
            try:
                return render(request, '500.html', status=500)
            except:
                # Fallback if template doesn't exist
                from django.http import HttpResponse
                return HttpResponse(
                    '<h1>Internal Server Error</h1><p>We apologize for the inconvenience.</p>',
                    status=500
                )
        
        return None