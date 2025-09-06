# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import HeroSlide

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'image_preview',
        'has_subtitle',
        'is_active',
        'order',
        'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    list_editable = ['is_active', 'order']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'image', 'image_preview')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Display a small preview of the image in admin"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 100px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"

    def has_subtitle(self, obj):
        """Show if the slide has a subtitle"""
        return bool(obj.subtitle)
    has_subtitle.boolean = True
    has_subtitle.short_description = "Has Subtitle"

    def get_queryset(self, request):
        """Order by order field and creation date"""
        return super().get_queryset(request).order_by('order', '-created_at')

    class Media:
        css = {
            'all': ('admin/css/hero_admin.css',)
        }
        js = ('admin/js/hero_admin.js',)

# Customize admin site header
admin.site.site_header = "HSMS Admin Panel"
admin.site.site_title = "HSMS Admin"
admin.site.index_title = "Welcome to HSMS Administration"