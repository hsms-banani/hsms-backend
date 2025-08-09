# offices/serializers.py
from rest_framework import serializers
from .models import Secretary, Committee

class SecretarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretary
        fields = ['id', 'name', 'bio', 'email', 'phone']

class CommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = ['id', 'name', 'description', 'members']