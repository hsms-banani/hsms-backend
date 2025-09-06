"""
URL configuration for hsms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
<<<<<<< HEAD
# hsms/urls.py - Update your main URLs file

=======
# hsms/urls.py - CORRECTED VERSION
>>>>>>> 1ec4ac0a13ca208754d746c157c9fc6d929e54f6
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD
from django.contrib.sitemaps.views import sitemap
from seminary.sitemaps import (
    StaticViewSitemap,
    PageSitemap,
    NewsSitemap,
    EventSitemap,
    PublicationSitemap,
    FacultySitemap,
    GallerySitemap
)

# Set the admin site header
admin.site.site_header = "Holy Spirit Major Seminary Administration"

sitemaps = {
    'static': StaticViewSitemap,
    'pages': PageSitemap,
    'news': NewsSitemap,
    'events': EventSitemap,
    'publications': PublicationSitemap,
    'faculty': FacultySitemap,
    'galleries': GallerySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Dashboard URLs
    path('dashboard/', include('dashboard.urls')),
    
    # Library URLs
    path('library/', include('library.urls')),  # Add this line
    
    # Seminary URLs (keep as default)
    path('', include('seminary.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
from django.views.static import serve
from django.http import HttpResponse
import os

def serve_pdf(request, path):
    """Custom view to serve PDF files with proper headers for iframe embedding"""
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(full_path) and path.lower().endswith('.pdf'):
        with open(full_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="{}"'.format(os.path.basename(path))
            if settings.DEBUG:
                response['X-Frame-Options'] = 'ALLOWALL'
            else:
                response['X-Frame-Options'] = 'SAMEORIGIN'
            return response
    return serve(request, path, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    
    # Frontend routes
    path('', include('apps.home.urls')),
    # IMPORTANT: About routes need to come AFTER API routes to avoid conflicts
    path('api/news/', include('apps.news.api_urls')),
    path('api/academics/', include('apps.academics.api_urls')),
    path('api/publications/', include('apps.publications.urls')),
    path('students/api/students/', include('apps.students.api_urls')),
    
    # About API routes - MUST be before frontend about routes
    path('about/', include('apps.about.urls')),  # This includes the API routes
    
    # Other frontend routes
    path('our-seminary/', include('apps.seminary.urls')),
    path('academics/', include('apps.academics.urls')),
    path('offices/', include('apps.offices.urls')),
    path('publications/', include('apps.publications.urls')),
    path('students/', include('apps.students.urls')),
    path('announcements/', include('apps.announcements.urls')),
    path('hero/', include('apps.hero.urls')),
    path('news/', include('apps.news.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>', serve_pdf, name='serve_pdf'),
    ]
>>>>>>> 1ec4ac0a13ca208754d746c157c9fc6d929e54f6
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)