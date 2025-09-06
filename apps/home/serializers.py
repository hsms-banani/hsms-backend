# home/serializers.py
from rest_framework import serializers
from .models import HomeContent

class HomeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeContent
        fields = ['id', 'title', 'description', 'image']