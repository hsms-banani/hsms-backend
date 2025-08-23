# File: seminary/context_processors.py

from django.utils import timezone
from .models import SiteSettings, Announcement, Page

def site_settings(request):
    """Make site settings available globally"""
    try:
        settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings = None
    
    return {
        'site_settings': settings
    }

def global_announcements(request):
    """Make current announcements available globally"""
    current_announcements = Announcement.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).order_by('priority', '-created_at')[:3]
    
    return {
        'global_announcements': current_announcements
    }

def navigation_pages(request):
    """Make navigation pages available globally"""
    # Seminary pages for dropdown menu
    seminary_pages = Page.objects.filter(
        is_published=True,
        slug__in=[
            'rector-welcome', 
            'mission-vision', 
            'seminary-history', 
            'formation-program', 
            'rules-regulations'
        ]
    ).order_by('order')
    
    # HSIT pages for dropdown menu
    hsit_pages = Page.objects.filter(
        is_published=True,
        slug__in=[
            'director-message',
            'philosophy-department', 
            'theology-department',
            'academic-calendar',
            'library'
        ]
    ).order_by('order')
    
    # History & Heritage pages
    history_pages = Page.objects.filter(
        is_published=True,
        slug__in=[
            'church-history',
            'bangladesh-history',
            'local-church-history'
        ]
    ).order_by('order')
    
    # Spiritual Food pages
    spiritual_pages = Page.objects.filter(
        is_published=True,
        slug__in=[
            'prayer-services',
            'homilies',
            'spiritual-directors-desk'
        ]
    ).order_by('order')
    
    return {
        'seminary_nav_pages': seminary_pages,
        'hsit_nav_pages': hsit_pages,
        'history_nav_pages': history_pages,
        'spiritual_nav_pages': spiritual_pages,
    }

def breadcrumb_helper(request):
    """Helper for generating breadcrumbs"""
    def get_breadcrumbs(page_title, section=None):
        breadcrumbs = [('Home', 'home')]
        
        if section:
            if section == 'seminary':
                breadcrumbs.append(('Our Seminary', 'about_seminary'))
            elif section == 'hsit':
                breadcrumbs.append(('HSIT', 'hsit_about'))
            elif section == 'history':
                breadcrumbs.append(('History & Heritage', 'history_heritage'))
            elif section == 'spiritual':
                breadcrumbs.append(('Spiritual Food', 'spiritual_food'))
            elif section == 'news':
                breadcrumbs.append(('News', 'news_list'))
            elif section == 'events':
                breadcrumbs.append(('Events', 'events_list'))
            elif section == 'publications':
                breadcrumbs.append(('Publications', 'publications'))
            elif section == 'gallery':
                breadcrumbs.append(('Gallery', 'gallery_list'))
        
        breadcrumbs.append((page_title, None))
        return breadcrumbs
    
    return {
        'get_breadcrumbs': get_breadcrumbs
    }