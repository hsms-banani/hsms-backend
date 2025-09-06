# library/templatetags/search_tags.py

from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='highlight')
def highlight(text, query):
    """
    Highlights the query in the text.
    """
    if not query or not text:
        return text
    
    # Split query into words for better matching
    query_words = query.strip().split()
    highlighted_text = str(text)
    
    for word in query_words:
        if len(word) > 1:  # Only highlight words with 2+ characters
            # Use regex to find all occurrences of the word (case-insensitive)
            # and wrap them in a <mark> tag.
            pattern = re.escape(word)
            highlighted_text = re.sub(
                f'({pattern})', 
                r'<mark class="bg-yellow-200 px-1 rounded">\1</mark>', 
                highlighted_text, 
                flags=re.IGNORECASE
            )
    
    return mark_safe(highlighted_text)