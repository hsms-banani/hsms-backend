# Create this file: apps/about/management/commands/debug_rector.py
from django.core.management.base import BaseCommand
from apps.about.models import RectorMessage, RectorMessageParagraph, FeaturedSection

class Command(BaseCommand):
    help = 'Debug rector message data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Debugging Rector Message Data'))
        
        # Check Featured Section
        self.stdout.write('\n📋 Featured Sections:')
        featured_sections = FeaturedSection.objects.all()
        if featured_sections.exists():
            for section in featured_sections:
                self.stdout.write(f"  - {section.title} (Active: {section.is_active})")
        else:
            self.stdout.write(self.style.WARNING("  No featured sections found!"))
        
        # Check Rector Messages
        self.stdout.write('\n👨‍💼 Rector Messages:')
        rectors = RectorMessage.objects.all()
        if rectors.exists():
            for rector in rectors:
                self.stdout.write(f"  - {rector.name} (Active: {rector.is_active})")
                self.stdout.write(f"    Position: {rector.position}")
                self.stdout.write(f"    Image: {rector.image}")
                self.stdout.write(f"    Quote: {rector.quote[:50]}..." if rector.quote else "    Quote: None")
                
                # Check paragraphs
                paragraphs = RectorMessageParagraph.objects.filter(rector_message=rector)
                self.stdout.write(f"    Paragraphs: {paragraphs.count()}")
                for i, p in enumerate(paragraphs.order_by('order')):
                    self.stdout.write(f"      {i+1}. (Order: {p.order}, Active: {p.is_active}) {p.content[:100]}...")
        else:
            self.stdout.write(self.style.WARNING("  No rector messages found!"))
        
        # Test API data
        self.stdout.write('\n🔧 Testing API Data Generation:')
        try:
            from apps.about.api_views import get_media_url
            
            active_rector = RectorMessage.objects.filter(is_active=True).first()
            if active_rector:
                self.stdout.write(f"  ✅ Active rector found: {active_rector.name}")
                
                paragraphs = RectorMessageParagraph.objects.filter(
                    rector_message=active_rector,
                    is_active=True
                ).order_by('order')
                
                self.stdout.write(f"  ✅ Active paragraphs: {paragraphs.count()}")
                
                paragraph_contents = [p.content for p in paragraphs]
                
                api_data = {
                    'id': active_rector.id,
                    'name': active_rector.name,
                    'position': active_rector.position,
                    'image_url': get_media_url(active_rector.image),
                    'quote': active_rector.quote or '',
                    'message_paragraph_1': paragraph_contents[0] if len(paragraph_contents) > 0 else '',
                    'message_paragraph_2': paragraph_contents[1] if len(paragraph_contents) > 1 else '',
                }
                
                self.stdout.write('  📊 API Data Preview:')
                for key, value in api_data.items():
                    if isinstance(value, str) and len(value) > 100:
                        self.stdout.write(f"    {key}: {value[:100]}...")
                    else:
                        self.stdout.write(f"    {key}: {value}")
                        
            else:
                self.stdout.write(self.style.ERROR("  ❌ No active rector found!"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ❌ Error generating API data: {e}"))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Debug complete!'))