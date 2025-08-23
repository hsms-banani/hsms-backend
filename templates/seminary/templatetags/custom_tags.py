from django import template
import re

register = template.Library()

@register.filter
def youtube_id(url):
    """Extract YouTube video ID from URL"""
    if not url:
        return ''
    
    # Handle different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return ''

@register.filter
def vimeo_id(url):
    """Extract Vimeo video ID from URL"""
    if not url:
        return ''
    
    # Handle different Vimeo URL formats
    patterns = [
        r'vimeo\.com\/(\d+)',
        r'player\.vimeo\.com\/video\/(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return ''

@register.filter
def is_youtube(url):
    """Check if URL is a YouTube video"""
    if not url:
        return False
    return 'youtube.com' in url or 'youtu.be' in url

@register.filter
def is_vimeo(url):
    """Check if URL is a Vimeo video"""
    if not url:
        return False
    return 'vimeo.com' in url

@register.filter
def truncate_chars(value, max_length):
    """Truncate string to specified character length"""
    if len(value) <= max_length:
        return value
    return value[:max_length] + '...'

@register.filter
def gallery_type_icon(gallery_type):
    """Return appropriate icon for gallery type"""
    icons = {
        'photo': 'fas fa-images',
        'video': 'fas fa-video',
    }
    return icons.get(gallery_type, 'fas fa-folder')

@register.simple_tag
def gallery_item_count(gallery, item_type=None):
    """Get count of items in gallery, optionally filtered by type"""
    if not gallery:
        return 0
    
    items = gallery.items.all()
    
    if item_type == 'image':
        items = items.exclude(image__isnull=True).exclude(image='')
    elif item_type == 'video':
        items = items.filter(
            models.Q(video_url__isnull=False) | 
            models.Q(video_file__isnull=False)
        ).exclude(video_url='')
    
    return items.count()

@register.inclusion_tag('seminary/partials/gallery_card.html')
def render_gallery_card(gallery, show_type=True):
    """Render a gallery card component"""
    return {
        'gallery': gallery,
        'show_type': show_type,
        'item_count': gallery.items.count(),
    }