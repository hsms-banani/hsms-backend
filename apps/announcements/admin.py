# apps/announcements/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'is_active', 
        'priority', 
        'has_attachment',
        'start_date', 
        'end_date', 
        'created_at'
    ]
    list_filter = ['is_active', 'priority', 'created_at', 'start_date']
    search_fields = ['title', 'content']
    list_editable = ['is_active', 'priority']
    ordering = ['-priority', '-created_at']
    readonly_fields = ['created_at', 'updated_at', 'attachment_preview']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content')
        }),
        ('Attachment', {
            'fields': ('attachment', 'attachment_preview'),
            'description': 'Upload files like PDFs, images, documents, etc.'
        }),
        ('Settings', {
            'fields': ('is_active', 'priority')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date'),
            'description': 'Control when this announcement should be displayed'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_attachment(self, obj):
        """Display whether announcement has an attachment"""
        if obj.attachment:
            return format_html(
                '<span style="color: green;">✓ Yes</span>'
            )
        return format_html('<span style="color: red;">✗ No</span>')
    has_attachment.short_description = 'Attachment'
    has_attachment.admin_order_field = 'attachment'

    def attachment_preview(self, obj):
        """Show attachment preview in admin"""
        if obj.attachment:
            file_url = obj.attachment.url
            file_name = obj.attachment.name.split('/')[-1]
            
            # Check if it's an image
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                return format_html(
                    '<div style="margin: 10px 0;">'
                    '<p><strong>File:</strong> <a href="{}" target="_blank">{}</a></p>'
                    '<img src="{}" style="max-width: 200px; max-height: 200px; border: 1px solid #ddd; padding: 5px;" />'
                    '</div>',
                    file_url, file_name, file_url
                )
            else:
                return format_html(
                    '<div style="margin: 10px 0;">'
                    '<p><strong>File:</strong> <a href="{}" target="_blank">{}</a></p>'
                    '<p><em>Click the link above to download/view the file</em></p>'
                    '</div>',
                    file_url, file_name
                )
        return "No attachment"
    attachment_preview.short_description = 'Attachment Preview'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Optional: Custom admin site configuration
admin.site.site_header = "HSMS Administration"
admin.site.site_title = "HSMS Admin Portal"
admin.site.index_title = "Welcome to HSMS Administration"