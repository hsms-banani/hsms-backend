# apps/about/api_views.py - Updated with content cleaning
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.utils import timezone
import logging
import traceback

from .models import (
    FeaturedSection, RectorMessage, RectorMessageParagraph,
    AcademicDepartment, FormationStep, CommitteeOffice
)
from .utils import clean_summernote_content, process_content_for_display

# Set up logging
logger = logging.getLogger(__name__)

def get_media_url(image_field):
    """Helper function to get full media URL"""
    if image_field and hasattr(image_field, 'url'):
        base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        return f"{base_url}{image_field.url}"
    return None

def clean_content_for_api(content):
    """Clean content specifically for API responses"""
    if not content:
        return ""
    
    # Clean the content using our utility function
    cleaned_content = clean_summernote_content(content)
    
    # Additional API-specific cleaning
    # Remove any remaining problematic elements
    import re
    
    # Remove any remaining style attributes that might have been missed
    cleaned_content = re.sub(r'&lt;style&gt;.*?&lt;/style&gt;', '', cleaned_content, flags=re.IGNORECASE | re.DOTALL)
    cleaned_content = re.sub(r'&lt;.*?&gt;', '', cleaned_content)  # Remove encoded HTML tags
    
    # Clean up any remaining Microsoft Word artifacts
    cleaned_content = re.sub(r'mso-[^;]*:[^;]*;?', '', cleaned_content, flags=re.IGNORECASE)
    
    # Normalize whitespace
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()
    
    return cleaned_content

@require_http_methods(["GET", "OPTIONS"])
@cache_control(no_cache=True, must_revalidate=True)
def featured_complete_api(request):
    """API endpoint for complete featured section data with cleaned content"""
    
    # Handle OPTIONS request for CORS preflight
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    try:
        logger.info("Featured complete API called")
        
        # Initialize response data
        response_data = {
            'section_info': None,
            'rector_message': None,
            'departments': [],
            'formation_steps': [],
            'committees_offices': [],
            'success': True,
            'debug': {
                'message': 'API endpoint reached successfully',
                'timestamp': str(timezone.now()),
                'content_cleaning': 'enabled'
            }
        }
        
        # Get section info
        try:
            featured_section = FeaturedSection.objects.filter(is_active=True).first()
            if featured_section:
                response_data['section_info'] = {
                    'title': featured_section.title,
                    'subtitle': featured_section.subtitle,
                }
                logger.info(f"Found featured section: {featured_section.title}")
            else:
                logger.warning("No active featured section found")
        except Exception as e:
            logger.error(f"Error fetching featured section: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

        # Get rector message with cleaned paragraphs
        try:
            logger.info("Attempting to fetch rector message...")
            rector = RectorMessage.objects.filter(is_active=True).first()
            
            if rector:
                logger.info(f"Found active rector: {rector.name}")
                
                # Get all paragraphs ordered by order field
                paragraphs = RectorMessageParagraph.objects.filter(
                    rector_message=rector,
                    is_active=True
                ).order_by('order')
                
                logger.info(f"Found {paragraphs.count()} active paragraphs for rector")
                
                # Clean paragraph contents
                paragraph_contents = []
                for i, p in enumerate(paragraphs):
                    # Clean the content before adding to response
                    raw_content = p.content or ''
                    cleaned_content = clean_content_for_api(raw_content)
                    paragraph_contents.append(cleaned_content)
                    
                    logger.info(f"Paragraph {i}: original length={len(raw_content)}, cleaned length={len(cleaned_content)}, order={p.order}")
                
                # Build rector message data with cleaned content
                response_data['rector_message'] = {
                    'id': rector.id,
                    'name': rector.name,
                    'position': rector.position,
                    'image_url': get_media_url(rector.image),
                    'quote': rector.quote or '',
                    'message_paragraph_1': paragraph_contents[0] if len(paragraph_contents) > 0 else '',
                    'message_paragraph_2': paragraph_contents[1] if len(paragraph_contents) > 1 else '',
                    'all_paragraphs': [
                        {
                            'content': clean_content_for_api(p.content), 
                            'order': p.order, 
                            'id': p.id
                        } 
                        for p in paragraphs
                    ]
                }
                
                logger.info(f"Rector message data prepared successfully for: {rector.name}")
                logger.info(f"Quote length: {len(rector.quote or '')}")
                logger.info(f"Cleaned paragraph 1 length: {len(paragraph_contents[0] if paragraph_contents else '')}")
                logger.info(f"Cleaned paragraph 2 length: {len(paragraph_contents[1] if len(paragraph_contents) > 1 else '')}")
                
            else:
                logger.warning("No active rector message found in database")
                # Add debug info about what's in the database
                all_rectors = RectorMessage.objects.all()
                logger.info(f"Total rector messages in DB: {all_rectors.count()}")
                for r in all_rectors:
                    logger.info(f"Rector: {r.name}, Active: {r.is_active}")
                
        except Exception as e:
            logger.error(f"Error fetching rector message: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            response_data['debug']['rector_error'] = str(e)

        # Get departments with features
        try:
            dept_queryset = AcademicDepartment.objects.filter(is_active=True).order_by('order', 'name')
            logger.info(f"Found {dept_queryset.count()} active departments")
            
            for dept in dept_queryset:
                features = [{
                    'id': f.id,
                    'title': f.title,
                    'order': f.order
                } for f in dept.features.all().order_by('order')]
                
                response_data['departments'].append({
                    'id': dept.id,
                    'name': dept.name,
                    'display_name': dept.display_name,
                    'image_url': get_media_url(dept.image),
                    'description': dept.description,
                    'link_url': dept.link_url,
                    'features': features
                })
        except Exception as e:
            logger.error(f"Error fetching departments: {str(e)}")
            response_data['debug']['departments_error'] = str(e)

        # Get formation steps
        try:
            steps_queryset = FormationStep.objects.filter(is_active=True).order_by('step_number')
            response_data['formation_steps'] = [{
                'id': step.id,
                'step_number': step.step_number,
                'title': step.title,
                'description': step.description
            } for step in steps_queryset]
            logger.info(f"Found {len(response_data['formation_steps'])} formation steps")
        except Exception as e:
            logger.error(f"Error fetching formation steps: {str(e)}")
            response_data['debug']['formation_error'] = str(e)

        # Get committees and offices
        try:
            committees_queryset = CommitteeOffice.objects.filter(is_active=True).order_by('order', 'title')
            response_data['committees_offices'] = [{
                'id': office.id,
                'title': office.title,
                'description': office.description,
                'icon': office.icon,
                'link_url': office.link_url
            } for office in committees_queryset]
            logger.info(f"Found {len(response_data['committees_offices'])} committees/offices")
        except Exception as e:
            logger.error(f"Error fetching committees/offices: {str(e)}")
            response_data['debug']['committees_error'] = str(e)

        # Final logging
        logger.info(f"API response prepared - Rector message present: {bool(response_data['rector_message'])}")
        if response_data['rector_message']:
            logger.info(f"Rector: {response_data['rector_message']['name']}")
        
        # Create response with CORS headers
        response = JsonResponse(response_data, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        response["Content-Type"] = "application/json"
        
        return response

    except Exception as e:
        logger.error(f"Unexpected error in featured_complete_api: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        error_response = {
            'error': 'Internal server error',
            'detail': str(e),
            'success': False,
            'debug': {
                'traceback': traceback.format_exc() if settings.DEBUG else 'Enable DEBUG for traceback'
            }
        }
        
        response = JsonResponse(error_response, status=500)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

@require_http_methods(["GET", "OPTIONS"])
@cache_control(no_cache=True, must_revalidate=True)
def rector_message_api(request):
    """API endpoint for just rector message data with cleaned content"""
    
    # Handle OPTIONS request for CORS preflight
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    try:
        logger.info("Rector message API called")
        
        response_data = {
            'rector_message': None,
            'success': True,
            'debug': {
                'message': 'Rector message API endpoint reached',
                'content_cleaning': 'enabled'
            }
        }
        
        rector = RectorMessage.objects.filter(is_active=True).first()
        
        if rector:
            logger.info(f"Found active rector: {rector.name}")
            
            # Get all paragraphs ordered by order field
            paragraphs = RectorMessageParagraph.objects.filter(
                rector_message=rector,
                is_active=True
            ).order_by('order')
            
            logger.info(f"Found {paragraphs.count()} active paragraphs")
            
            # Clean paragraph contents
            paragraph_contents = [clean_content_for_api(p.content) for p in paragraphs]
            
            response_data['rector_message'] = {
                'id': rector.id,
                'name': rector.name,
                'position': rector.position,
                'image_url': get_media_url(rector.image),
                'quote': rector.quote or '',
                'message_paragraph_1': paragraph_contents[0] if len(paragraph_contents) > 0 else '',
                'message_paragraph_2': paragraph_contents[1] if len(paragraph_contents) > 1 else '',
                'all_paragraphs': [
                    {
                        'content': clean_content_for_api(p.content), 
                        'order': p.order, 
                        'id': p.id
                    } 
                    for p in paragraphs
                ]
            }
            
            logger.info(f"Rector message prepared successfully with cleaned content")
        else:
            logger.warning("No active rector message found")
            response_data['debug']['warning'] = 'No active rector message in database'

        response = JsonResponse(response_data, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        
        return response

    except Exception as e:
        logger.error(f"Error in rector_message_api: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        error_response = {
            'error': 'Internal server error',
            'detail': str(e),
            'success': False,
            'debug': {
                'traceback': traceback.format_exc() if settings.DEBUG else 'Enable DEBUG for traceback'
            }
        }
        
        response = JsonResponse(error_response, status=500)
        response["Access-Control-Allow-Origin"] = "*"
        return response