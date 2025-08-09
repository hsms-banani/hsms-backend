# apps/announcements/serializers.py
from rest_framework import serializers
from .models import Announcement
import os

class AnnouncementSerializer(serializers.ModelSerializer):
    attachment_url = serializers.SerializerMethodField()
    attachment_name = serializers.ReadOnlyField()
    attachment_size = serializers.ReadOnlyField()
    attachment_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'priority', 'created_at', 
            'updated_at', 'start_date', 'end_date', 'attachment', 
            'attachment_url', 'attachment_name', 'attachment_size', 'attachment_type'
        ]
    
    def get_attachment_url(self, obj):
        if obj.attachment:
            request = self.context.get('request')
            if request:
                # Return full URL including domain
                return request.build_absolute_uri(obj.attachment.url)
            return obj.attachment.url
        return None
    
    def get_attachment_type(self, obj):
        if obj.attachment:
            ext = os.path.splitext(obj.attachment.name)[1].lower()
            
            # Image types
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
                return 'image'
            # PDF
            elif ext == '.pdf':
                return 'pdf'
            # Document types
            elif ext in ['.doc', '.docx', '.txt', '.rtf']:
                return 'document'
            # Spreadsheet types
            elif ext in ['.xls', '.xlsx', '.csv']:
                return 'spreadsheet'
            # Presentation types
            elif ext in ['.ppt', '.pptx']:
                return 'presentation'
            # Archive types
            elif ext in ['.zip', '.rar', '.7z']:
                return 'archive'
            # Media types
            elif ext in ['.mp3', '.wav', '.mp4', '.avi', '.mov']:
                return 'media'
            else:
                return 'other'
        return None