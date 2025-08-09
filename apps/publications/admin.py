# publications/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import AnkurPublication, DipttoSakhyoPublication

@admin.register(AnkurPublication)
class AnkurPublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_size', 'download_count', 'is_featured', 'date_published', 'pdf_preview']
    list_filter = ['is_featured', 'date_published']
    search_fields = ['title']
    readonly_fields = ['download_count', 'file_size', 'date_published', 'date_updated']
    list_editable = ['is_featured']
    
    fieldsets = (
        ('Publication Info', {
            'fields': ('title', 'pdf_file', 'thumbnail')
        }),
        ('Status', {
            'fields': ('is_featured',)
        }),
        ('Statistics', {
            'fields': ('download_count', 'file_size', 'date_published', 'date_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def pdf_preview(self, obj):
        if obj.pdf_file:
            return format_html(
                '<a href="{}" target="_blank" class="button">View PDF</a>',
                obj.pdf_file.url
            )
        return "No file"
    pdf_preview.short_description = "PDF File"

@admin.register(DipttoSakhyoPublication)
class DipttoSakhyoPublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'issue', 'file_size', 'download_count', 'is_featured', 'date_published', 'pdf_preview']
    list_filter = ['is_featured', 'date_published', 'issue']
    search_fields = ['title', 'issue']
    readonly_fields = ['download_count', 'file_size', 'date_published', 'date_updated']
    list_editable = ['is_featured']
    
    fieldsets = (
        ('Publication Info', {
            'fields': ('title', 'issue', 'pdf_file', 'thumbnail')
        }),
        ('Status', {
            'fields': ('is_featured',)
        }),
        ('Statistics', {
            'fields': ('download_count', 'file_size', 'date_published', 'date_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def pdf_preview(self, obj):
        if obj.pdf_file:
            return format_html(
                '<a href="{}" target="_blank" class="button">View PDF</a>',
                obj.pdf_file.url
            )
        return "No file"
    pdf_preview.short_description = "PDF File"