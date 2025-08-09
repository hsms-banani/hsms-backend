# apps/home/urls.py
from django.urls import path
from apps.home.views import HomeContentList  # Add 'apps.' prefix

urlpatterns = [
    path('api/home/', HomeContentList.as_view(), name='home-content'),
]