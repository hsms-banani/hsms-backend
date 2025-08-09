# academics/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    # Your existing models
    FacultyMember, Professor, CourseDescription, ResearchPaper, Thesis,
    # New models
    AcademicYear, EventCategory, CalendarEvent, CalendarSettings
)
@admin.register(FacultyMember)
class FacultyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'email', 'created_at')
    list_filter = ('designation', 'created_at')
    search_fields = ('name', 'designation', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'designation', 'email', 'image')
        }),
        ('Details', {
            'fields': ('bio',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'email', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('name', 'department', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'department', 'email', 'image')
        }),
        ('Details', {
            'fields': ('bio',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CourseDescription)
class CourseDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'author')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Paper Information', {
            'fields': ('title', 'author', 'file')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'author')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Thesis Information', {
            'fields': ('title', 'author', 'file')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date', 'is_current', 'is_active', 'events_count')
    list_filter = ('is_current', 'is_active', 'start_date')
    search_fields = ('year',)
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_current', 'is_active')
    
    fieldsets = (
        ('Academic Year Information', {
            'fields': ('year', 'start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('is_current', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def events_count(self, obj):
        count = obj.events.count()
        if count > 0:
            url = reverse('admin:academics_calendarevent_changelist') + f'?academic_year__id={obj.id}'
            return format_html('<a href="{}">{} events</a>', url, count)
        return count
    events_count.short_description = 'Events'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_preview', 'events_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'color', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'

    def events_count(self, obj):
        count = obj.events.count()
        if count > 0:
            url = reverse('admin:academics_calendarevent_changelist') + f'?category__id={obj.id}'
            return format_html('<a href="{}">{} events</a>', url, count)
        return count
    events_count.short_description = 'Events'

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'category_colored', 'start_date', 'end_date', 
                   'priority', 'is_published', 'is_featured', 'academic_year')
    list_filter = ('event_type', 'category', 'priority', 'is_published', 'is_featured', 
                  'academic_year', 'start_date', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at', 'duration_info')
    list_editable = ('is_published', 'is_featured', 'priority')
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'event_type', 'category', 'academic_year')
        }),
        ('Date and Time', {
            'fields': ('start_date', 'end_date', 'is_all_day', 'start_time', 'end_time')
        }),
        ('Additional Details', {
            'fields': ('location', 'priority')
        }),
        ('Recurrence', {
            'fields': ('is_recurring', 'recurrence_pattern'),
            'classes': ('collapse',)
        }),
        ('Status and Visibility', {
            'fields': ('is_published', 'is_featured', 'created_by')
        }),
        ('System Information', {
            'fields': ('duration_info', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def category_colored(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            obj.category.color,
            obj.category.name
        )
    category_colored.short_description = 'Category'

    def duration_info(self, obj):
        if obj.is_multi_day:
            return f"{obj.duration_days} days ({obj.start_date} to {obj.end_date})"
        return f"Single day ({obj.start_date})"
    duration_info.short_description = 'Duration'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'academic_year')

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.created_by = request.user.username
        super().save_model(request, obj, form, change)

    class Media:
        js = ('admin/js/calendar_admin.js',)  # You can add custom JS if needed

@admin.register(CalendarSettings)
class CalendarSettingsAdmin(admin.ModelAdmin):
    list_display = ('default_academic_year', 'default_view', 'events_per_page', 
                   'show_weekends', 'allow_public_view')
    fieldsets = (
        ('Display Settings', {
            'fields': ('default_academic_year', 'default_view', 'events_per_page', 'show_weekends')
        }),
        ('Access Settings', {
            'fields': ('allow_public_view',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        # Only allow one settings instance
        return not CalendarSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of settings
        return False

# Inline admin for events within academic year
class CalendarEventInline(admin.TabularInline):
    model = CalendarEvent
    extra = 0
    fields = ('title', 'event_type', 'start_date', 'end_date', 'is_published')
    readonly_fields = ('title',)
    show_change_link = True