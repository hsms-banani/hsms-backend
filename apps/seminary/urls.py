# seminary/urls.py
from django.urls import path
from .views import (
    ChurchHistoryList, BangladeshHistoryList,
    LocalChurchHistoryList, SeminaryHistoryList,
    DepartmentList, FormationProgramList
)

urlpatterns = [
    path('api/seminary/church-history/', ChurchHistoryList.as_view(), name='church-history'),
    path('api/seminary/bangladesh-history/', BangladeshHistoryList.as_view(), name='bangladesh-history'),
    path('api/seminary/local-church-history/', LocalChurchHistoryList.as_view(), name='local-church-history'),
    path('api/seminary/seminary-history/', SeminaryHistoryList.as_view(), name='seminary-history'),
    path('api/seminary/departments/', DepartmentList.as_view(), name='departments'),
    path('api/seminary/formation-program/', FormationProgramList.as_view(), name='formation-program'),
]