# events/serializers.py
from rest_framework import serializers
from .models import Event, PhotoGallery, VideoGallery

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'event_type', 'date', 'description', 'location', 'is_upcoming']

class PhotoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoGallery
        fields = ['id', 'image', 'caption', 'event']

class VideoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGallery
        fields = ['id', 'video_url', 'caption', 'event']