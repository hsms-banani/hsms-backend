# about/serializers.py
from rest_framework import serializers
from .models import (
    AboutSection, AcademicAuthority, MissionVision,
    AcademicCalendar, History, Formation, RulesRegulations,
    FeaturedSection, RectorMessage, RectorMessageParagraph,
    AcademicDepartment, DepartmentFeature, FormationStep, CommitteeOffice
)

class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = ['id', 'title', 'content']

class AcademicAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicAuthority
        fields = ['id', 'name', 'position', 'bio']

class MissionVisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionVision
        fields = ['id', 'mission', 'vision']

class AcademicCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCalendar
        fields = ['id', 'year', 'file']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'title', 'content']

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = ['id', 'title', 'content']

class RulesRegulationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RulesRegulations
        fields = ['id', 'title', 'content']

class FeaturedSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedSection
        fields = ['id', 'title', 'subtitle', 'is_active', 'created_at', 'updated_at']

class RectorMessageParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = RectorMessageParagraph
        fields = ['id', 'content', 'order', 'is_active', 'created_at', 'updated_at']

class RectorMessageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    paragraphs = RectorMessageParagraphSerializer(many=True, read_only=True)
    
    class Meta:
        model = RectorMessage
        fields = [
            'id', 'name', 'position', 'image', 'image_url', 'quote', 
            'paragraphs', 'is_active', 'created_at', 'updated_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class DepartmentFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentFeature
        fields = ['id', 'title', 'order']

class AcademicDepartmentSerializer(serializers.ModelSerializer):
    features = DepartmentFeatureSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AcademicDepartment
        fields = [
            'id', 'name', 'display_name', 'image', 'image_url', 'description', 
            'link_url', 'order', 'is_active', 'features', 'created_at', 'updated_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class FormationStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormationStep
        fields = [
            'id', 'step_number', 'title', 'description', 'is_active',
            'created_at', 'updated_at'
        ]

class CommitteeOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeOffice
        fields = [
            'id', 'title', 'description', 'icon', 'link_url', 'order', 
            'is_active', 'created_at', 'updated_at'
        ]

class FeaturedSectionCompleteSerializer(serializers.Serializer):
    """Complete serializer that combines all featured section data"""
    section_info = FeaturedSectionSerializer(read_only=True)
    rector_message = RectorMessageSerializer(read_only=True)
    departments = AcademicDepartmentSerializer(many=True, read_only=True)
    formation_steps = FormationStepSerializer(many=True, read_only=True)
    committees_offices = CommitteeOfficeSerializer(many=True, read_only=True)