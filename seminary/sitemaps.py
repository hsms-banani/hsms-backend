from django.contrib.sitemaps import Sitemap
from .models import Page, News, Event, Publication, Faculty, Gallery

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'about_seminary', 'contact', 'news_list', 'events_list', 'publications', 'gallery_list', 'faculty_list']

    def location(self, item):
        from django.urls import reverse
        return reverse(item)

class PageSitemap(Sitemap):
    def items(self):
        return Page.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

class NewsSitemap(Sitemap):
    def items(self):
        return News.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

class EventSitemap(Sitemap):
    def items(self):
        return Event.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at

class PublicationSitemap(Sitemap):
    def items(self):
        return Publication.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at

class FacultySitemap(Sitemap):
    def items(self):
        return Faculty.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.joined_date

class GallerySitemap(Sitemap):
    def items(self):
        return Gallery.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at
