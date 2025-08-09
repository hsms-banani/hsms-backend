# seminary/views.py
from rest_framework import generics
from .models import (
    ChurchHistory, BangladeshHistory, LocalChurchHistory,
    SeminaryHistory, Department, FormationProgram
)
from .serializers import (
    ChurchHistorySerializer, BangladeshHistorySerializer,
    LocalChurchHistorySerializer, SeminaryHistorySerializer,
    DepartmentSerializer, FormationProgramSerializer
)

class ChurchHistoryList(generics.ListAPIView):
    queryset = ChurchHistory.objects.all()
    serializer_class = ChurchHistorySerializer

class BangladeshHistoryList(generics.ListAPIView):
    queryset = BangladeshHistory.objects.all()
    serializer_class = BangladeshHistorySerializer

class LocalChurchHistoryList(generics.ListAPIView):
    queryset = LocalChurchHistory.objects.all()
    serializer_class = LocalChurchHistorySerializer

class SeminaryHistoryList(generics.ListAPIView):
    queryset = SeminaryHistory.objects.all()
    serializer_class = SeminaryHistorySerializer

class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class FormationProgramList(generics.ListAPIView):
    queryset = FormationProgram.objects.all()
    serializer_class = FormationProgramSerializer