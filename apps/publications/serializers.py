# publications/serializers.py
from rest_framework import serializers
from .models import AnkurPublication, DipttoSakhyoPublication

class AnkurPublicationSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    
    class Meta:
        model = AnkurPublication
        fields = [
            'id', 
            'title', 
            'pdf_file', 
            'file_url',
            'thumbnail',
            'thumbnail_url',
            'date_published',
            'formatted_date',
            'is_featured',
            'download_count',
            'file_size'
        ]
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file and request:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None
    
    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None
    
    def get_formatted_date(self, obj):
        return obj.date_published.strftime('%B %d, %Y')

class DipttoSakhyoPublicationSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    
    class Meta:
        model = DipttoSakhyoPublication
        fields = [
            'id', 
            'title', 
            'issue',
            'pdf_file', 
            'file_url',
            'thumbnail',
            'thumbnail_url',
            'date_published',
            'formatted_date',
            'is_featured',
            'download_count',
            'file_size'
        ]
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file and request:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None
    
    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None
    
    def get_formatted_date(self, obj):
        return obj.date_published.strftime('%B %d, %Y')