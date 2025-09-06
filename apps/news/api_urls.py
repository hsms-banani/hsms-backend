# apps/news/api_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListAPIView.as_view(), name='news-list-api'),
    path('latest/', views.latest_news, name='latest-news-api'),
    path('categories/', views.NewsCategoryAPIView.as_view(), name='news-categories-api'),
    path('<slug:slug>/', views.NewsDetailAPIView.as_view(), name='news-detail-api'),
]

