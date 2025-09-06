# academics/api_urls.py

from django.urls import path
from .views import (
    # Your existing views
    FacultyMemberList, FacultyMemberDetail,
    ProfessorList, ProfessorDetail,
    CourseDescriptionList, CourseDescriptionDetail,
    ResearchPaperList, ResearchPaperDetail,
    ThesisList, ThesisDetail,
    # New calendar views
    AcademicYearListView, AcademicYearDetailView,
    EventCategoryListView,
    CalendarEventListView, CalendarEventDetailView,
    CalendarEventCreateView, CalendarEventUpdateView, CalendarEventDeleteView,
    upcoming_events, current_events, monthly_calendar,
    events_by_category, event_statistics, calendar_settings,
    search_events, events_feed
)

urlpatterns = [
    # Your existing endpoints
    # Faculty Members endpoints
    path('faculties/members/', FacultyMemberList.as_view(), name='api-faculty-members'),
    path('faculties/members/<int:pk>/', FacultyMemberDetail.as_view(), name='api-faculty-member-detail'),
    
    # Professors endpoints
    path('faculties/professors/', ProfessorList.as_view(), name='api-professors-list'),
    path('faculties/professors/<int:pk>/', ProfessorDetail.as_view(), name='api-professor-detail'),
    
    # Course descriptions endpoints
    path('faculties/courses/', CourseDescriptionList.as_view(), name='api-course-descriptions'),
    path('faculties/courses/<int:pk>/', CourseDescriptionDetail.as_view(), name='api-course-description-detail'),
    
    # Research papers endpoints
    path('professors-corner/research-papers/', ResearchPaperList.as_view(), name='api-research-papers'),
    path('professors-corner/research-papers/<int:pk>/', ResearchPaperDetail.as_view(), name='api-research-paper-detail'),
    
    # Theses endpoints
    path('professors-corner/theses/', ThesisList.as_view(), name='api-theses'),
    path('professors-corner/theses/<int:pk>/', ThesisDetail.as_view(), name='api-thesis-detail'),
    
    # NEW ACADEMIC CALENDAR ENDPOINTS
    
    # Academic Years
    path('calendar/academic-years/', AcademicYearListView.as_view(), name='api-academic-years'),
    path('calendar/academic-years/<int:pk>/', AcademicYearDetailView.as_view(), name='api-academic-year-detail'),
    
    # Event Categories
    path('calendar/categories/', EventCategoryListView.as_view(), name='api-event-categories'),
    
    # Calendar Events - CRUD operations
    path('calendar/events/', CalendarEventListView.as_view(), name='api-calendar-events'),
    path('calendar/events/<int:pk>/', CalendarEventDetailView.as_view(), name='api-calendar-event-detail'),
    path('calendar/events/create/', CalendarEventCreateView.as_view(), name='api-calendar-event-create'),
    path('calendar/events/<int:pk>/update/', CalendarEventUpdateView.as_view(), name='api-calendar-event-update'),
    path('calendar/events/<int:pk>/delete/', CalendarEventDeleteView.as_view(), name='api-calendar-event-delete'),
    
    # Calendar Views and Utilities
    path('calendar/upcoming/', upcoming_events, name='api-upcoming-events'),
    path('calendar/current/', current_events, name='api-current-events'),
    path('calendar/month/<int:year>/<int:month>/', monthly_calendar, name='api-monthly-calendar'),
    path('calendar/by-category/', events_by_category, name='api-events-by-category'),
    path('calendar/statistics/', event_statistics, name='api-event-statistics'),
    path('calendar/settings/', calendar_settings, name='api-calendar-settings'),
    path('calendar/search/', search_events, name='api-search-events'),
    path('calendar/feed/', events_feed, name='api-events-feed'),
]