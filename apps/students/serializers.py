# students/serializers.py
from rest_framework import serializers
from .models import (
    Student, EnrollmentRequirement, ExamInformation,
    TuitionFee, Document, FAQ, SpiritualGuidance
)

class StudentSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'name', 'congregation', 'diocese', 'year_joined',
            'student_id', 'email', 'phone', 'photo', 'photo_url', 'status'
        ]
    
    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None

class EnrollmentRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRequirement
        fields = ['id', 'title', 'description', 'is_mandatory', 'order']

class ExamInformationSerializer(serializers.ModelSerializer):
    exam_datetime = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamInformation
        fields = [
            'id', 'title', 'description', 'exam_date', 'exam_time',
            'location', 'exam_type', 'exam_datetime'
        ]
    
    def get_exam_datetime(self, obj):
        if obj.exam_time:
            return f"{obj.exam_date} {obj.exam_time}"
        return str(obj.exam_date)

class TuitionFeeSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = TuitionFee
        fields = [
            'id', 'title', 'amount', 'formatted_amount', 'description',
            'academic_year', 'fee_type', 'due_date'
        ]
    
    def get_formatted_amount(self, obj):
        return f"${obj.amount:,.2f}"

class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_size_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'file', 'file_url', 'category', 'description',
            'is_required', 'file_size', 'file_size_formatted'
        ]
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def get_file_size_formatted(self, obj):
        if obj.file_size:
            if obj.file_size < 1024 * 1024:  # Less than 1MB
                return f"{obj.file_size / 1024:.1f} KB"
            else:
                return f"{obj.file_size / (1024 * 1024):.1f} MB"
        return None

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'is_featured']

class SpiritualGuidanceSerializer(serializers.ModelSerializer):
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = SpiritualGuidance
        fields = [
            'id', 'title', 'content', 'excerpt', 'author',
            'category', 'is_featured', 'created_at'
        ]
    
    def get_excerpt(self, obj):
        return obj.content[:200] + "..." if len(obj.content) > 200 else obj.content