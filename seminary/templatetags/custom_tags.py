from django import template
import re

register = template.Library()

@register.filter(name='youtube_id')
def youtube_id(value):
    """Extracts the YouTube video ID from a URL."""
    match = re.search(r'(?:v=|/|embed/|youtu.be/)([^&?#]+)', value)
    return match.group(1) if match else None

@register.filter(name='vimeo_id')
def vimeo_id(value):
    """Extracts the Vimeo video ID from a URL."""
    match = re.search(r'(?:vimeo.com/|player.vimeo.com/video/)(\d+)', value)
    return match.group(1) if match else None

@register.filter(name='split')
def split(value, delimiter=','):
    """Split a string by delimiter and return a list of stripped items"""
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter)]