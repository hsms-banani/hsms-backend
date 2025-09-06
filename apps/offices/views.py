# offices/views.py
from rest_framework import generics
from .models import Secretary, Committee
from .serializers import SecretarySerializer, CommitteeSerializer

class SecretaryList(generics.ListAPIView):
    queryset = Secretary.objects.all()
    serializer_class = SecretarySerializer

class CommitteeList(generics.ListAPIView):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer