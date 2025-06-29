# Create/Replace suggestor/middleware.py with this comprehensive version:

import time
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.urls import resolve
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs

class ComprehensiveActivityMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        # Record start time for response time calculation
        request._start_time = time.time()
        
        # Skip tracking for certain paths
        skip_paths = ['/static/', '/media/', '/favicon.ico', '/admin/jsi18n/']
        if any(request.path.startswith(path) for path in skip_paths):
            return None
        
        # Only track authenticated users
        if not request.user.is_authenticated:
            return None
        
        # Store previous page for time-on-page calculation
        if hasattr(request.user, '_last_page_time'):
            time_on_previous = time.time() - request.user._last_page_time
            request._time_on_previous_page = time_on_previous
        request.user._last_page_time = time.time()
        
        return None
    
    def process_response(self, request, response):
        # Skip if not tracking this request
        if (not hasattr(request, '_start_time') or 
            not request.user.is_authenticated or
            any(request.path.startswith(path) for path in ['/static/', '/media/', '/favicon.ico'])):
            return response
        
        try:
            self.log_activity(request, response)
        except Exception as e:
            # Don't break the request if logging fails
            print(f"Activity logging error: {e}")
        
        return response
    
    def log_activity(self, request, response):
        from .models import UserActivity
        
        # Calculate response time
        response_time = time.time() - request._start_time
        
        # Determine action type
        action = self.determine_action(request, response)
        if not action:
            return
        
        # Get basic request info
        activity_data = {
            'user': request.user,
            'action': action,
            'session_id': request.session.session_key,
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500],
            'page_url': request.build_absolute_uri(),
            'referrer': request.META.get('HTTP_REFERER', ''),
            'request_method': request.method,
            'response_time': response_time,
            'response_size': len(response.content) if hasattr(response, 'content') else None,
        }
        
        # Add time on previous page
        if hasattr(request, '_time_on_previous_page'):
            from datetime import timedelta
            activity_data['time_on_page'] = timedelta(seconds=request._time_on_previous_page)
        
        # Add specific action details
        self.add_action_specific_data(request, response, activity_data)
        
        # Create the activity record
        try:
            activity = UserActivity(**activity_data)
            activity._session_key = request.session.session_key
            activity.save()
        except Exception as e:
            print(f"Failed to save activity: {e}")
    
    def determine_action(self, request, response):
        path = request.path
        method = request.method
        
        # Skip AJAX requests and API calls unless they're important
        if (request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 
            not any(important in path for important in ['/suggest/', '/search/', '/filter/'])):
            return None
        
        # Determine action based on path and method
        if method == 'GET':
            if path == '/':
                return 'page_view'
            elif '/tlr/' in path and path.endswith('/'):
                return 'view_tlr'
            elif '/download/' in path:
                return 'download_tlr'
            elif '/results/' in path:
                return 'search'
            elif '/filter/' in path or '/suggest/' in path:
                return 'filter_applied'
            elif path.startswith('/admin/'):
                return None  # Skip admin pages (logged separately)
            else:
                return 'page_view'
        
        elif method == 'POST':
            if '/suggest/' in path or '/search/' in path:
                return 'search'
            elif '/filter/' in path:
                return 'filter_applied'
            elif 'route' in path or 'select' in path:
                return 'route_selected'
            else:
                return 'form_submitted'
        
        return 'page_view'
    
    def add_action_specific_data(self, request, response, activity_data):
        action = activity_data['action']
        
        # Handle TLR-related actions
        if action in ['view_tlr', 'download_tlr']:
            tlr = self.get_tlr_from_request(request)
            if tlr:
                activity_data['tlr'] = tlr
        
        # Handle search actions
        elif action == 'search':
            search_query = (request.GET.get('q') or 
                          request.POST.get('keywords') or 
                          request.POST.get('search_query', ''))
            if search_query:
                activity_data['search_query'] = search_query
                # Try to get result count from response
                activity_data['search_results_count'] = self.extract_result_count(response)
        
        # Handle filter actions
        elif action == 'filter_applied':
            filters = {}
            if request.method == 'POST':
                filters = {k: v for k, v in request.POST.items() 
                          if k not in ['csrfmiddlewaretoken', 'route']}
            else:
                filters = dict(request.GET)
            
            if filters:
                activity_data['filters_applied'] = filters
        
        # Handle route selection
        elif action == 'route_selected':
            route = request.POST.get('route') or request.GET.get('route')
            if route:
                activity_data['route_selected'] = route
        
        # Handle form submissions
        elif action == 'form_submitted':
            # Safely capture form data (excluding sensitive fields)
            safe_fields = {}
            excluded_fields = ['password', 'csrfmiddlewaretoken', 'password1', 'password2']
            
            for key, value in request.POST.items():
                if key.lower() not in excluded_fields:
                    safe_fields[key] = value if len(str(value)) < 200 else str(value)[:200] + "..."
            
            if safe_fields:
                activity_data['form_data'] = safe_fields
        
        # Handle errors
        if hasattr(response, 'status_code') and response.status_code >= 400:
            activity_data['action'] = 'error_encountered'
            activity_data['error_code'] = str(response.status_code)
            if hasattr(response, 'content'):
                # Try to extract error message
                content = response.content.decode('utf-8', errors='ignore')[:500]
                activity_data['error_message'] = content
    
    def get_tlr_from_request(self, request):
        try:
            # Try to extract TLR ID or slug from URL
            resolver_match = resolve(request.path)
            tlr_identifier = (resolver_match.kwargs.get('pk') or 
                             resolver_match.kwargs.get('slug'))
            
            if tlr_identifier:
                from .models import Tlr
                try:
                    if tlr_identifier.isdigit():
                        return Tlr.objects.get(pk=tlr_identifier)
                    else:
                        return Tlr.objects.get(slug=tlr_identifier)
                except Tlr.DoesNotExist:
                    pass
        except Exception:
            pass
        return None
    
    def extract_result_count(self, response):
        """Try to extract search result count from response"""
        try:
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8', errors='ignore')
                # Look for common patterns like "X results found"
                import re
                patterns = [
                    r'(\d+)\s+results?',
                    r'Found\s+(\d+)',
                    r'(\d+)\s+TLRs?\s+found',
                ]
                for pattern in patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        return int(match.group(1))
        except Exception:
            pass
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# Signal handlers for login/logout with enhanced tracking
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    from .models import UserActivity
    
    middleware = ComprehensiveActivityMiddleware(None)
    activity = UserActivity(
        user=user,
        action='login',
        session_id=request.session.session_key,
        ip_address=middleware.get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
        page_url=request.build_absolute_uri(),
        referrer=request.META.get('HTTP_REFERER', ''),
        request_method=request.method
    )
    activity._session_key = request.session.session_key
    activity.save()

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user:
        from .models import UserActivity
        
        middleware = ComprehensiveActivityMiddleware(None)
        activity = UserActivity(
            user=user,
            action='logout',
            session_id=getattr(request.session, 'session_key', ''),
            ip_address=middleware.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            page_url=request.build_absolute_uri(),
            request_method=request.method
        )
        activity.save()