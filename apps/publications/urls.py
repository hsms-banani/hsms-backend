# publications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # List views
    path('ankur/', views.AnkurPublicationList.as_view(), name='ankur-list'),
    path('diptto-sakhyo/', views.DipttoSakhyoPublicationList.as_view(), name='diptto-sakhyo-list'),
    
    # Detail views
    path('ankur/<int:pk>/', views.AnkurPublicationDetail.as_view(), name='ankur-detail'),
    path('diptto-sakhyo/<int:pk>/', views.DipttoSakhyoPublicationDetail.as_view(), name='diptto-sakhyo-detail'),
    
    # Download tracking
    path('ankur/<int:pk>/download/', views.download_ankur_publication, name='ankur-download'),
    path('diptto-sakhyo/<int:pk>/download/', views.download_diptto_sakhyo_publication, name='diptto-sakhyo-download'),
]