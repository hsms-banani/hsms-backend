# apps/news/serializers.py
from rest_framework import serializers
from .models import News, NewsCategory

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name', 'slug', 'description']

class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer(read_only=True)
    author_name = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'image_url',
            'category', 'author_name', 'status', 'featured', 'views_count',
            'created_at', 'updated_at', 'published_at', 'read_time',
            'meta_title', 'meta_description', 'meta_keywords'
        ]
    
    def get_author_name(self, obj):
        """Get the full name of the author, fallback to username"""
        if hasattr(obj.author, 'get_full_name'):
            full_name = obj.author.get_full_name()
            if full_name.strip():
                return full_name
        return obj.author.username
    
    def get_read_time(self, obj):
        """Estimate read time (average 200 words per minute)"""
        if obj.content:
            # Remove HTML tags for word count
            import re
            text = re.sub(r'<[^>]+>', '', obj.content)
            word_count = len(text.split())
            read_time = max(1, word_count // 200)
            return read_time
        return 1
    
    def get_image_url(self, obj):
        """Get the full URL for the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None