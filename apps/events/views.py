# events/views.py
from rest_framework import generics
from django.utils import timezone
from .models import Event, PhotoGallery, VideoGallery
from .serializers import EventSerializer, PhotoGallerySerializer, VideoGallerySerializer

class UpcomingSeminarsList(generics.ListAPIView):
    serializer_class = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(
            event_type='seminar',
            date__gte=timezone.now(),
            is_upcoming=True
        )

class UpcomingProgramsList(generics.ListAPIView):
    serializer_class = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(
            event_type='program',
            date__gte=timezone.now(),
            is_upcoming=True
        )

class PhotoGalleryList(generics.ListAPIView):
    serializer_class = PhotoGallerySerializer
    queryset = PhotoGallery.objects.all()

class VideoGalleryList(generics.ListAPIView):
    serializer_class = VideoGallerySerializer
    queryset = VideoGallery.objects.all()