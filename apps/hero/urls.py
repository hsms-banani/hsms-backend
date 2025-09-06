from django.urls import path
from . import views

app_name = 'hero'

urlpatterns = [
    # API endpoints for frontend consumption
    path('api/hero-slides/', views.HeroSlideListView.as_view(), name='hero-slides-list'),
    path('api/hero-slides/<int:id>/', views.HeroSlideDetailView.as_view(), name='hero-slide-detail'),
    
    # CRUD API endpoints
    path('api/hero-slides/create/', views.HeroSlideCreateView.as_view(), name='hero-slide-create'),
    path('api/hero-slides/<int:id>/update/', views.HeroSlideUpdateView.as_view(), name='hero-slide-update'),
    path('api/hero-slides/<int:id>/delete/', views.HeroSlideDeleteView.as_view(), name='hero-slide-delete'),
    
    # Function-based view alternatives
    path('api/active-slides/', views.get_active_hero_slides, name='active-hero-slides'),
    path('api/slide/<int:slide_id>/', views.get_hero_slide_by_id, name='hero-slide-by-id'),
]