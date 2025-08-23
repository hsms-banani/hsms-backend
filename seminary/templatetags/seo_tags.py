
import json
from django import template
from django.utils.safestring import mark_safe
from seminary.models import SiteSettings

register = template.Library()

@register.simple_tag(takes_context=True)
def schema_markup(context):
    request = context.get('request')
    if not request:
        return ''

    site_settings = SiteSettings.objects.first()
    if not site_settings:
        return ''

    schema = {
        "@context": "https://schema.org",
        "@type": "CollegeOrUniversity",
        "name": site_settings.site_name,
        "alternateName": "Banani Seminary",
        "url": "https://hsms-banani.org/",
        "logo": request.build_absolute_uri(site_settings.site_logo.url) if site_settings.site_logo else '',
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": site_settings.phone,
            "contactType": "customer service",
            "email": site_settings.email
        },
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Block A-112, Road 27, Banani",
            "addressLocality": "Dhaka",
            "postalCode": "1213",
            "addressCountry": "BD"
        },
        "sameAs": [
            site_settings.facebook_url,
            site_settings.instagram_url,
            site_settings.youtube_url
        ]
    }

    # Page-specific schema
    if 'page' in context:
        page = context['page']
        schema.update({
            "@type": "WebPage",
            "headline": page.title,
            "description": page.meta_description or page.excerpt,
            "url": request.build_absolute_uri(page.get_absolute_url()),
        })

    if 'news_item' in context:
        news_item = context['news_item']
        schema.update({
            "@type": "NewsArticle",
            "headline": news_item.title,
            "image": [request.build_absolute_uri(news_item.featured_image.url)] if news_item.featured_image else [],
            "datePublished": news_item.publish_date.isoformat() if news_item.publish_date else news_item.created_at.isoformat(),
            "dateModified": news_item.updated_at.isoformat(),
            "author": {
                "@type": "Person",
                "name": news_item.author.get_full_name() if news_item.author else site_settings.site_name
            },
            "publisher": {
                "@type": "Organization",
                "name": site_settings.site_name,
                "logo": {
                    "@type": "ImageObject",
                    "url": request.build_absolute_uri(site_settings.site_logo.url) if site_settings.site_logo else ''
                }
            },
            "description": news_item.meta_description or news_item.excerpt
        })

    if 'event' in context:
        event = context['event']
        schema.update({
            "@type": "Event",
            "name": event.title,
            "startDate": event.start_date.isoformat(),
            "endDate": event.end_date.isoformat() if event.end_date else None,
            "location": {
                "@type": "Place",
                "name": event.location,
                "address": event.location
            },
            "description": event.description,
            "image": [request.build_absolute_uri(event.featured_image.url)] if event.featured_image else [],
            "organizer": {
                "@type": "Organization",
                "name": event.organizer or site_settings.site_name
            }
        })

    if 'faculty' in context:
        faculty = context['faculty']
        schema.update({
            "@type": "Person",
            "name": faculty.name,
            "jobTitle": faculty.title,
            "worksFor": {
                "@type": "CollegeOrUniversity",
                "name": site_settings.site_name
            },
            "image": request.build_absolute_uri(faculty.photo.url) if faculty.photo else '',
            "email": faculty.email,
            "telephone": faculty.phone
        })

    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema)}</script>')
