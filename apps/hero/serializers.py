# serializers.py
from rest_framework import serializers
from .models import HeroSlide

class HeroSlideSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSlide
        fields = [
            'id',
            'title',
            'subtitle',
            'image',
            'image_url',
            'is_active',
            'order',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        """Return the full URL of the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class HeroSlideListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing active slides"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSlide
        fields = [
            'id',
            'title',
            'subtitle',
            'image_url',
            'order'
        ]

    def get_image_url(self, obj):
        """Return the full URL of the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None