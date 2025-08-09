# academics/urls.py
from django.urls import path
from .views import (
    FacultyMemberList, FacultyMemberDetail,
    ProfessorList, ProfessorDetail,
    CourseDescriptionList, CourseDescriptionDetail,
    ResearchPaperList, ResearchPaperDetail,
    ThesisList, ThesisDetail
)

urlpatterns = [
    # Faculty Members endpoints
    path('api/academics/faculties/members/', FacultyMemberList.as_view(), name='faculty-members'),
    path('api/academics/faculties/members/<int:pk>/', FacultyMemberDetail.as_view(), name='faculty-member-detail'),
    
    # Professors endpoints
    path('api/academics/faculties/professors/', ProfessorList.as_view(), name='professors-list'),
    path('api/academics/faculties/professors/<int:pk>/', ProfessorDetail.as_view(), name='professor-detail'),
    
    # Course descriptions endpoints
    path('api/academics/faculties/courses/', CourseDescriptionList.as_view(), name='course-descriptions'),
    path('api/academics/faculties/courses/<int:pk>/', CourseDescriptionDetail.as_view(), name='course-description-detail'),
    
    # Research papers endpoints
    path('api/academics/professors-corner/research-papers/', ResearchPaperList.as_view(), name='research-papers'),
    path('api/academics/professors-corner/research-papers/<int:pk>/', ResearchPaperDetail.as_view(), name='research-paper-detail'),
    
    # Theses endpoints
    path('api/academics/professors-corner/theses/', ThesisList.as_view(), name='theses'),
    path('api/academics/professors-corner/theses/<int:pk>/', ThesisDetail.as_view(), name='thesis-detail'),
]