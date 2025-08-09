# offices/urls.py
from django.urls import path
from .views import SecretaryList, CommitteeList

urlpatterns = [
    path('api/offices/secretary/', SecretaryList.as_view(), name='secretary'),
    path('api/offices/committees/', CommitteeList.as_view(), name='committees'),
]