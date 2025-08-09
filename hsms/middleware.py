# hsms/middleware.py
from django.conf import settings

class CacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add cache control headers for API endpoints in development
        if settings.DEBUG and request.path.startswith('/hero/api/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            
        return response

class PDFFrameMiddleware:
    """
    Middleware to handle PDF file serving with proper headers for iframe embedding
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if this is a PDF file request
        if (request.path.startswith('/media/') and 
            request.path.lower().endswith('.pdf')):
            
            # Remove restrictive frame options for PDF files in development
            if settings.DEBUG:
                response['X-Frame-Options'] = 'ALLOWALL'
            else:
                response['X-Frame-Options'] = 'SAMEORIGIN'
                
            # Add proper PDF headers
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = 'inline'
            
        return response