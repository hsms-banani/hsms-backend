# apps/announcements/views.py
from rest_framework import generics
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Announcement
from .serializers import AnnouncementSerializer

class ActiveAnnouncementsView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    
    def get_queryset(self):
        now = timezone.now()
        return Announcement.objects.filter(
            is_active=True,
            start_date__lte=now
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        ).order_by('-priority', '-created_at')

class AnnouncementDetailView(generics.RetrieveAPIView):
    """
    Returns a single announcement by ID
    """
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.filter(is_active=True)
    lookup_field = 'id'

class AnnouncementTickerView(generics.GenericAPIView):
    """
    Returns announcements formatted for the news ticker
    """
    def get(self, request):
        now = timezone.now()
        announcements = Announcement.objects.filter(
            is_active=True,
            start_date__lte=now
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        ).order_by('-priority', '-created_at')
        
        # Format announcements for ticker - using title instead of content
        ticker_items = []
        for ann in announcements:
            ticker_items.append({
                'id': ann.id,
                'title': ann.title,
                'content': ann.content
            })
        
        ticker_text = ' • '.join([item['title'] for item in ticker_items])
        
        return Response({
            'ticker_text': ticker_text,
            'ticker_items': ticker_items,
            'announcements': AnnouncementSerializer(announcements, many=True, context={'request': request}).data
        })