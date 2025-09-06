# apps/about/admin.py - Updated with content cleaning and preview
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    AboutSection, AcademicAuthority, MissionVision,
    AcademicCalendar, History, Formation, RulesRegulations,
    FeaturedSection, RectorMessage, RectorMessageParagraph,
    AcademicDepartment, DepartmentFeature, FormationStep, CommitteeOffice
)
from .utils import clean_summernote_content, extract_plain_text

# Inline for Rector Message Paragraphs
class RectorMessageParagraphInline(admin.TabularInline):
    model = RectorMessageParagraph
    extra = 1
    fields = ('order', 'content_preview', 'content', 'is_active')
    readonly_fields = ('content_preview',)
    ordering = ['order']
    
    def content_preview(self, obj):
        """Show a clean preview of the content"""
        if obj.content:
            plain_text = extract_plain_text(obj.content, 100)
            return format_html('<div style="max-width: 300px; font-style: italic;">{}</div>', plain_text)
        return "No content"
    content_preview.short_description = "Content Preview"
    
    class Meta:
        verbose_name = "Message Paragraph"
        verbose_name_plural = "Message Paragraphs"

# Inline for Department Features
class DepartmentFeatureInline(admin.TabularInline):
    model = DepartmentFeature
    extra = 1
    fields = ('title', 'order')
    ordering = ['order']

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(AcademicAuthority)
class AcademicAuthorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name', 'position')

@admin.register(MissionVision)
class MissionVisionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

@admin.register(AcademicCalendar)
class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('year', 'file')
    list_filter = ('year',)

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(RulesRegulations)
class RulesRegulationsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(FeaturedSection)
class FeaturedSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(RectorMessage)
class RectorMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'paragraph_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'position')
    readonly_fields = ('created_at', 'updated_at', 'paragraph_count')
    inlines = [RectorMessageParagraphInline]
    
    def paragraph_count(self, obj):
        """Show number of active paragraphs"""
        count = obj.paragraphs.filter(is_active=True).count()
        return format_html('<span style="font-weight: bold;">{}</span>', count)
    paragraph_count.short_description = "Active Paragraphs"
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'image', 'is_active'),
            'description': 'Basic rector information and profile image'
        }),
        ('Quote', {
            'fields': ('quote',),
            'description': 'Optional inspirational quote (leave blank to hide quote section)'
        }),
        ('Statistics', {
            'fields': ('paragraph_count',),
            'classes': ('collapse',),
            'description': 'Content statistics'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(RectorMessageParagraph)
class RectorMessageParagraphAdmin(SummernoteModelAdmin):
    list_display = ('rector_message', 'order', 'content_preview', 'word_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'rector_message', 'created_at')
    search_fields = ('rector_message__name', 'content')
    list_editable = ('order', 'is_active')
    ordering = ('rector_message', 'order')
    readonly_fields = ('created_at', 'updated_at', 'content_preview', 'word_count', 'cleaned_content_preview')
    
    summernote_fields = ('content',)
    
    def content_preview(self, obj):
        """Show a clean preview of the content"""
        if obj.content:
            plain_text = extract_plain_text(obj.content, 150)
            return format_html('<div style="max-width: 400px; padding: 10px; background: #f8f9fa; border-radius: 5px; font-style: italic;">{}</div>', plain_text)
        return "No content"
    content_preview.short_description = "Content Preview"
    
    def word_count(self, obj):
        """Show word count"""
        if obj.content:
            plain_text = extract_plain_text(obj.content)
            word_count = len(plain_text.split())
            color = "green" if word_count > 50 else "orange" if word_count > 20 else "red"
            return format_html('<span style="color: {}; font-weight: bold;">{} words</span>', color, word_count)
        return "0 words"
    word_count.short_description = "Word Count"
    
    def cleaned_content_preview(self, obj):
        """Show how the content will look after cleaning"""
        if obj.content:
            cleaned = clean_summernote_content(obj.content)
            # Show first 200 characters of cleaned content
            preview = cleaned[:200] + "..." if len(cleaned) > 200 else cleaned
            return format_html(
                '<div style="max-width: 500px; padding: 10px; background: #e8f5e8; border: 1px solid #4caf50; border-radius: 5px;">'
                '<strong>Cleaned Content:</strong><br>{}</div>', 
                preview
            )
        return "No content to clean"
    cleaned_content_preview.short_description = "Cleaned Content Preview"
    
    fieldsets = (
        ('Paragraph Details', {
            'fields': ('rector_message', 'order', 'is_active'),
            'description': 'Basic paragraph settings'
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Use the rich text editor for formatting (bold, italic, colors, links, etc.)'
        }),
        ('Content Analysis', {
            'fields': ('content_preview', 'word_count', 'cleaned_content_preview'),
            'classes': ('collapse',),
            'description': 'Content analysis and cleaning preview'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Clean content before saving and show success message"""
        if obj.content:
            original_content = obj.content
            obj.content = clean_summernote_content(obj.content)
            
            # Show message if content was cleaned
            if original_content != obj.content:
                self.message_user(
                    request, 
                    f"Content was automatically cleaned to remove unwanted formatting for paragraph {obj.order + 1}.",
                    level='success'
                )
        
        super().save_model(request, obj, form, change)

@admin.register(AcademicDepartment)
class AcademicDepartmentAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'order', 'feature_count', 'is_active', 'created_at')
    list_filter = ('name', 'is_active', 'created_at')
    search_fields = ('display_name', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    inlines = [DepartmentFeatureInline]
    readonly_fields = ('created_at', 'updated_at', 'feature_count')
    
    def feature_count(self, obj):
        """Show number of features"""
        count = obj.features.count()
        return format_html('<span style="font-weight: bold;">{}</span>', count)
    feature_count.short_description = "Features"
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'display_name', 'image', 'description', 'link_url')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'feature_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(FormationStep)
class FormationStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    ordering = ('step_number',)

@admin.register(CommitteeOffice)
class CommitteeOfficeAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order', 'is_active', 'created_at')
    list_filter = ('icon', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'title')

# Custom admin site header
admin.site.site_header = "HSMS Content Management"
admin.site.site_title = "HSMS Admin"
admin.site.index_title = "Welcome to HSMS Content Management System"