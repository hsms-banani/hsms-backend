# events/admin.py
from django.contrib import admin
from .models import Event, PhotoGallery, VideoGallery

admin.site.register(Event)
admin.site.register(PhotoGallery)
admin.site.register(VideoGallery)