# academics/serializers.py
from rest_framework import serializers
from datetime import date
from .models import (
    # Your existing models
    FacultyMember, Professor, CourseDescription, ResearchPaper, Thesis,
    # New models
    AcademicYear, EventCategory, CalendarEvent, CalendarSettings
)
class FacultyMemberSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FacultyMember
        fields = ['id', 'name', 'designation', 'bio', 'email', 'image', 'image_url', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class ProfessorSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Professor
        fields = ['id', 'name', 'department', 'bio', 'email', 'image', 'image_url', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class CourseDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDescription
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']

class ResearchPaperSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ResearchPaper
        fields = ['id', 'title', 'author', 'file', 'file_url', 'created_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

class ThesisSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Thesis
        fields = ['id', 'title', 'author', 'file', 'file_url', 'created_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
class AcademicYearSerializer(serializers.ModelSerializer):
    events_count = serializers.SerializerMethodField()
    is_past = serializers.SerializerMethodField()
    is_future = serializers.SerializerMethodField()

    class Meta:
        model = AcademicYear
        fields = ['id', 'year', 'start_date', 'end_date', 'is_current', 'is_active', 
                 'events_count', 'is_past', 'is_future', 'created_at', 'updated_at']

    def get_events_count(self, obj):
        return obj.events.filter(is_published=True).count()

    def get_is_past(self, obj):
        return obj.end_date < date.today()

    def get_is_future(self, obj):
        return obj.start_date > date.today()

class EventCategorySerializer(serializers.ModelSerializer):
    events_count = serializers.SerializerMethodField()

    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'color', 'description', 'is_active', 'events_count', 'created_at']

    def get_events_count(self, obj):
        return obj.events.filter(is_published=True).count()

class CalendarEventListSerializer(serializers.ModelSerializer):
    """Serializer for list view with minimal fields"""
    category = EventCategorySerializer(read_only=True)
    academic_year = serializers.StringRelatedField(read_only=True)
    duration_days = serializers.ReadOnlyField()
    is_multi_day = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    is_current = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'event_type', 'category', 'academic_year', 'start_date', 
                 'end_date', 'start_time', 'end_time', 'is_all_day', 'location', 'priority', 
                 'is_featured', 'duration_days', 'is_multi_day', 'is_past', 'is_current', 
                 'is_upcoming', 'formatted_date']

    def get_formatted_date(self, obj):
        if obj.is_multi_day:
            return f"{obj.start_date.strftime('%B %d')} - {obj.end_date.strftime('%B %d, %Y')}"
        else:
            return obj.start_date.strftime('%B %d, %Y')

class CalendarEventDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed view with all fields"""
    category = EventCategorySerializer(read_only=True)
    academic_year = AcademicYearSerializer(read_only=True)
    duration_days = serializers.ReadOnlyField()
    is_multi_day = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    is_current = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    formatted_date = serializers.SerializerMethodField()
    formatted_time = serializers.SerializerMethodField()

    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'description', 'event_type', 'category', 'academic_year',
                 'start_date', 'end_date', 'start_time', 'end_time', 'is_all_day', 'location',
                 'priority', 'is_recurring', 'recurrence_pattern', 'is_published', 'is_featured',
                 'created_by', 'duration_days', 'is_multi_day', 'is_past', 'is_current',
                 'is_upcoming', 'formatted_date', 'formatted_time', 'created_at', 'updated_at']

    def get_formatted_date(self, obj):
        if obj.is_multi_day:
            return f"{obj.start_date.strftime('%A, %B %d')} - {obj.end_date.strftime('%A, %B %d, %Y')}"
        else:
            return obj.start_date.strftime('%A, %B %d, %Y')

    def get_formatted_time(self, obj):
        if obj.is_all_day:
            return "All Day"
        elif obj.start_time and obj.end_time:
            return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"
        elif obj.start_time:
            return obj.start_time.strftime('%I:%M %p')
        return None

class CalendarEventCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating events"""
    
    class Meta:
        model = CalendarEvent
        fields = ['title', 'description', 'event_type', 'category', 'academic_year',
                 'start_date', 'end_date', 'start_time', 'end_time', 'is_all_day',
                 'location', 'priority', 'is_recurring', 'recurrence_pattern',
                 'is_published', 'is_featured']

    def validate(self, data):
        """Custom validation for event data"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        is_all_day = data.get('is_all_day', True)

        # Validate dates
        if end_date and start_date and start_date > end_date:
            raise serializers.ValidationError("End date must be after or equal to start date")

        # Validate times for same-day events
        if (not is_all_day and start_time and end_time and 
            start_date == end_date and start_time >= end_time):
            raise serializers.ValidationError(
                "End time must be after start time for same-day events"
            )

        return data

class CalendarSettingsSerializer(serializers.ModelSerializer):
    default_academic_year = AcademicYearSerializer(read_only=True)

    class Meta:
        model = CalendarSettings
        fields = ['id', 'default_academic_year', 'show_weekends', 'default_view',
                 'events_per_page', 'allow_public_view', 'created_at', 'updated_at']

# Additional serializers for specific use cases

class UpcomingEventsSerializer(serializers.ModelSerializer):
    """Serializer for upcoming events widget/dashboard"""
    category = EventCategorySerializer(read_only=True)
    days_until = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'event_type', 'category', 'start_date', 'end_date',
                 'is_all_day', 'start_time', 'priority', 'is_featured', 'days_until',
                 'formatted_date']

    def get_days_until(self, obj):
        today = date.today()
        if obj.start_date > today:
            return (obj.start_date - today).days
        return 0

    def get_formatted_date(self, obj):
        if obj.is_multi_day:
            return f"{obj.start_date.strftime('%b %d')} - {obj.end_date.strftime('%b %d')}"
        else:
            return obj.start_date.strftime('%b %d')

class MonthlyCalendarSerializer(serializers.ModelSerializer):
    """Serializer optimized for calendar grid view"""
    category_color = serializers.CharField(source='category.color', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'event_type', 'start_date', 'end_date', 'is_all_day',
                 'start_time', 'end_time', 'priority', 'is_featured', 'category_color',
                 'category_name']