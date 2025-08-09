# apps/announcements/urls.py
from django.urls import path
from .views import ActiveAnnouncementsView, AnnouncementTickerView, AnnouncementDetailView

app_name = 'announcements'

urlpatterns = [
    path('api/announcements/', ActiveAnnouncementsView.as_view(), name='active-announcements'),
    path('api/announcements/ticker/', AnnouncementTickerView.as_view(), name='announcement-ticker'),
    path('api/announcements/<int:id>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
]