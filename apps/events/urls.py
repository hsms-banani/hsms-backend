# events/urls.py
from django.urls import path
from .views import (
    UpcomingSeminarsList,
    UpcomingProgramsList,
    PhotoGalleryList,
    VideoGalleryList
)

urlpatterns = [
    path('api/events/upcoming/seminars/', UpcomingSeminarsList.as_view(), name='upcoming-seminars'),
    path('api/events/upcoming/programs/', UpcomingProgramsList.as_view(), name='upcoming-programs'),
    path('api/events/archive/photo-gallery/', PhotoGalleryList.as_view(), name='photo-gallery'),
    path('api/events/archive/video-gallery/', VideoGalleryList.as_view(), name='video-gallery'),
]