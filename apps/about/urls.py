# apps/about/urls.py - FIXED VERSION
from django.urls import path
from .views import (
    AboutSectionList, AcademicAuthorityList,
    MissionVisionList, AcademicCalendarList, HistoryList,
    FormationList, RulesRegulationsList,
    FeaturedSectionView, RectorMessageView, AcademicDepartmentView,
    FormationStepView, CommitteeOfficeView, FeaturedSectionCompleteView
)
from . import api_views

urlpatterns = [
    # Custom API Views (Function-based) - THESE ARE THE PRIMARY ENDPOINTS
    path('api/featured/complete/', api_views.featured_complete_api, name='featured_complete_api'),
    path('api/rector-message/', api_views.rector_message_api, name='rector_message_api'),
    
    # DRF Views - Secondary endpoints
    path('api/featured/section/', FeaturedSectionView.as_view(), name='featured-section'),
    path('api/featured/rector-message-drf/', RectorMessageView.as_view(), name='rector-message-drf'),
    path('api/featured/departments/', AcademicDepartmentView.as_view(), name='academic-departments'),
    path('api/featured/formation-steps/', FormationStepView.as_view(), name='formation-steps'),
    path('api/featured/committees-offices/', CommitteeOfficeView.as_view(), name='committees-offices'),
    path('api/featured/complete-drf/', FeaturedSectionCompleteView.as_view(), name='featured-complete-drf'),
    
    # Other existing URLs
    path('api/section/', AboutSectionList.as_view(), name='about-section'),
    path('api/academic-authorities/', AcademicAuthorityList.as_view(), name='academic-authorities'),
    path('api/mission-vision/', MissionVisionList.as_view(), name='mission-vision'),
    path('api/academic-calendar/', AcademicCalendarList.as_view(), name='academic-calendar'),
    path('api/history/', HistoryList.as_view(), name='history'),
    path('api/formation/', FormationList.as_view(), name='formation'),
    path('api/rules-regulations/', RulesRegulationsList.as_view(), name='rules-regulations'),
]