# Enhanced seminary/sitemaps.py for better SEO

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import Page, News, Event, Publication, Faculty, Gallery

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return [
            'home', 'about_seminary', 'contact', 
            # Our Seminary
            'rector_welcome', 'mission_vision', 'seminary_history', 
            'formation_program', 'rules_regulations', 'committees',
            # History & Heritage
            'history_heritage', 'church_history', 'bangladesh_history', 'local_church_history',
            # HSIT
            'hsit_about', 'director_message', 'philosophy_department', 'theology_department',
            'faculty_list', 'academic_calendar', 'course_descriptions', 'library',
            'student_list', 'enrollment_requirements', 'exam_information', 'tuition_fees',
            'forms_documents', 'faqs',
            # Publications
            'publications', 'ankur_publications', 'diptto_sakhyo_publications', 'prodipon_publications',
            # Spiritual Food
            'spiritual_food', 'prayer_services', 'homilies', 'spiritual_directors_desk',
            # News & Events
            'news_list', 'events_list',
            # Gallery
            'gallery_list', 'photo_gallery', 'video_gallery',
            # Legal
            'terms_of_service', 'privacy_policy', 'site_map'
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return timezone.now()

    def get_priority(self, item):
        """Set different priorities for different page types"""
        high_priority_pages = ['home', 'about_seminary', 'contact', 'hsit_about']
        if item in high_priority_pages:
            return 1.0
        elif 'faculty' in item or 'publications' in item:
            return 0.9
        else:
            return 0.8

class PageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Page.objects.filter(is_published=True).order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def priority(self, obj):
        # Higher priority for recently updated pages
        days_old = (timezone.now() - obj.updated_at).days
        if days_old < 30:
            return 0.9
        elif days_old < 90:
            return 0.8
        else:
            return 0.7

class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    limit = 1000

    def items(self):
        return News.objects.filter(is_published=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at

    def priority(self, obj):
        # Higher priority for recent news
        days_old = (timezone.now() - obj.created_at).days
        if days_old < 7:
            return 1.0
        elif days_old < 30:
            return 0.9
        elif days_old < 90:
            return 0.8
        else:
            return 0.6

class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    limit = 500

    def items(self):
        # Changed from event_date to start_date
        return Event.objects.filter(is_published=True).order_by('-start_date')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

    def priority(self, obj):
        # Higher priority for upcoming events
        # Handle both DateTimeField and DateField
        now = timezone.now()
        
        # Convert start_date to date if it's a datetime
        if hasattr(obj.start_date, 'date'):
            event_date = obj.start_date.date()
        else:
            event_date = obj.start_date
            
        if event_date >= now.date():
            return 1.0  # Upcoming events
        else:
            days_past = (now.date() - event_date).days
            if days_past < 30:
                return 0.8  # Recent past events
            else:
                return 0.6  # Older events

class PublicationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    limit = 1000

    def items(self):
        return Publication.objects.filter(is_published=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

    def priority(self, obj):
        # Higher priority for recent publications
        days_old = (timezone.now() - obj.created_at).days
        if days_old < 30:
            return 0.9
        elif days_old < 180:
            return 0.8
        else:
            return 0.7

class FacultySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Faculty.objects.filter(is_active=True).order_by('name')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.joined_date

    def priority(self, obj):
        # Higher priority for senior faculty or department heads
        if hasattr(obj, 'is_department_head') and obj.is_department_head:
            return 0.9
        else:
            return 0.8

class GallerySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Gallery.objects.filter(is_published=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

    def priority(self, obj):
        # Higher priority for recent galleries
        days_old = (timezone.now() - obj.created_at).days
        if days_old < 30:
            return 0.8
        elif days_old < 90:
            return 0.7
        else:
            return 0.6