# apps/about/utils.py - Content Cleaning Utilities
import re
import html
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

def clean_summernote_content(content):
    """
    Clean Summernote content by removing Microsoft Word styles, 
    unwanted HTML, and formatting issues.
    """
    if not content:
        return content
    
    # Remove HTML comments
    content = re.sub(r'<!--[\s\S]*?-->', '', content)
    
    # Remove style blocks completely
    content = re.sub(r'<style[\s\S]*?</style>', '', content, flags=re.IGNORECASE)
    
    # Remove script blocks
    content = re.sub(r'<script[\s\S]*?</script>', '', content, flags=re.IGNORECASE)
    
    # Remove Microsoft Office specific elements
    content = re.sub(r'<o:p[\s\S]*?</o:p>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</?o:\w+[^>]*/?>', '', content, flags=re.IGNORECASE)
    
    # Remove all inline styles
    content = re.sub(r'\s*style\s*=\s*"[^"]*"', '', content, flags=re.IGNORECASE)
    
    # Remove all CSS classes
    content = re.sub(r'\s*class\s*=\s*"[^"]*"', '', content, flags=re.IGNORECASE)
    
    # Remove Microsoft Office specific attributes
    mso_attributes = [
        'mso-[^=]*="[^"]*"',
        'lang="[^"]*"',
        'xml:lang="[^"]*"',
        'dir="[^"]*"'
    ]
    for attr in mso_attributes:
        content = re.sub(attr, '', content, flags=re.IGNORECASE)
    
    # Clean up font family specifications
    content = re.sub(r'font-family:\s*[^;]*;?', '', content, flags=re.IGNORECASE)
    
    # Remove empty attributes
    content = re.sub(r'\s+=""', '', content)
    
    # Clean up excessive whitespace in HTML
    content = re.sub(r'\s+', ' ', content)
    
    # Remove empty paragraphs
    content = re.sub(r'<p[^>]*>\s*</p>', '', content, flags=re.IGNORECASE)
    
    # Clean up spans with no content or attributes
    content = re.sub(r'<span>\s*</span>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<span\s*>\s*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*</span>', '', content, flags=re.IGNORECASE)
    
    # Normalize paragraph tags
    content = re.sub(r'<p[^>]*>', '<p>', content, flags=re.IGNORECASE)
    
    # Remove any remaining Word-specific tags
    word_tags = ['font', 'span']  # Add more as needed
    for tag in word_tags:
        # Remove opening tags with attributes
        content = re.sub(f'<{tag}[^>]*>', '', content, flags=re.IGNORECASE)
        # Remove closing tags
        content = re.sub(f'</{tag}>', '', content, flags=re.IGNORECASE)
    
    # Clean up multiple consecutive line breaks
    content = re.sub(r'(<br\s*/?>){3,}', '<br><br>', content, flags=re.IGNORECASE)
    
    # Final cleanup - remove extra spaces
    content = content.strip()
    
    return content

def sanitize_html_content(content):
    """
    Sanitize HTML content to only allow safe tags and attributes.
    """
    try:
        import bleach
        
        # Define allowed tags and attributes
        ALLOWED_TAGS = [
            'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'blockquote', 'a', 'img', 'table', 'thead', 'tbody',
            'tr', 'th', 'td', 'div'
        ]
        
        ALLOWED_ATTRIBUTES = {
            'a': ['href', 'title', 'target'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'table': ['border', 'cellpadding', 'cellspacing'],
            'th': ['scope', 'colspan', 'rowspan'],
            'td': ['colspan', 'rowspan'],
        }
        
        ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']
        
        # Clean the content
        cleaned_content = bleach.clean(
            content,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOLS,
            strip=True,
            strip_comments=True
        )
        
        return cleaned_content
        
    except ImportError:
        # Fallback if bleach is not installed
        return clean_summernote_content(content)

def process_content_for_display(content):
    """
    Process content for safe display in frontend.
    This function combines cleaning and sanitization.
    """
    if not content:
        return ""
    
    # First, clean the content
    cleaned = clean_summernote_content(content)
    
    # Then sanitize it
    sanitized = sanitize_html_content(cleaned)
    
    # Mark as safe for Django templates
    return mark_safe(sanitized)

def extract_plain_text(html_content, max_length=None):
    """
    Extract plain text from HTML content for previews or search.
    """
    if not html_content:
        return ""
    
    # Remove HTML tags
    text = strip_tags(html_content)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return text