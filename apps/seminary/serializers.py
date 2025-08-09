# seminary/serializers.py
from rest_framework import serializers
from .models import (
    ChurchHistory, BangladeshHistory, LocalChurchHistory,
    SeminaryHistory, Department, FormationProgram
)

class ChurchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurchHistory
        fields = ['id', 'title', 'content']

class BangladeshHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BangladeshHistory
        fields = ['id', 'title', 'content']

class LocalChurchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalChurchHistory
        fields = ['id', 'title', 'content']

class SeminaryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeminaryHistory
        fields = ['id', 'title', 'content']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']

class FormationProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormationProgram
        fields = ['id', 'title', 'content']