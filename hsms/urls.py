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
# hsms/urls.py - Update your main URLs file

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)