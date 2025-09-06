# home/views.py
from rest_framework import generics
from .models import HomeContent
from .serializers import HomeContentSerializer

class HomeContentList(generics.ListAPIView):
    queryset = HomeContent.objects.all()
    serializer_class = HomeContentSerializer