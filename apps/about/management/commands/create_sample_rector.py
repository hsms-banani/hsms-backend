# Create this file: apps/about/management/commands/create_sample_rector.py
from django.core.management.base import BaseCommand
from apps.about.models import RectorMessage, RectorMessageParagraph, FeaturedSection

class Command(BaseCommand):
    help = 'Create sample rector message data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Creating sample rector message data...'))
        
        # Create Featured Section
        featured_section, created = FeaturedSection.objects.get_or_create(
            defaults={
                'title': 'Excellence in Theological & Philosophical Education',
                'subtitle': 'Discover what makes Holy Spirit Major Seminary a center for spiritual and intellectual formation',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write('  ✅ Created featured section')
        else:
            self.stdout.write('  📋 Featured section already exists')
        
        # Create Rector Message
        rector, created = RectorMessage.objects.get_or_create(
            name="Rev. Fr. Paul Gomes",
            defaults={
                'position': 'Rector, Holy Spirit Major Seminary',
                'quote': 'Faith and reason illuminate the path to truth, guiding our students toward a deeper understanding of God\'s call in their lives.',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write('  ✅ Created rector message')
        else:
            self.stdout.write('  👨‍💼 Rector message already exists')
            # Make sure it's active
            rector.is_active = True
            rector.save()
        
        # Create Paragraphs
        paragraphs_data = [
            {
                'order': 0,
                'content': '''Welcome to Holy Spirit Major Seminary, where we have been forming future priests and lay ministers for over five decades. Our institution stands as a beacon of theological excellence and spiritual formation, dedicated to preparing servant-leaders who will serve the Church and society with wisdom, compassion, and integrity.
                
As we navigate the challenges of our contemporary world, we remain committed to our mission of providing comprehensive theological education that integrates academic rigor with deep spiritual formation. Our students engage with sacred scripture, church tradition, and modern theological scholarship while developing the pastoral skills necessary for effective ministry.'''
            },
            {
                'order': 1,
                'content': '''Our seminary community embraces diversity while maintaining unity in our common mission. We welcome seminarians from various cultural backgrounds, creating a rich tapestry of experiences that enriches our learning environment. Through prayer, study, and community life, we foster an atmosphere where future ministers can discern their calling and develop the skills needed to serve God's people effectively.

I encourage you to explore our website, visit our campus, and discover how Holy Spirit Major Seminary can be the place where your vocation flourishes. May God bless you on your journey of faith and service.'''
            }
        ]
        
        # Delete existing paragraphs for this rector to avoid duplicates
        RectorMessageParagraph.objects.filter(rector_message=rector).delete()
        
        # Create new paragraphs
        for para_data in paragraphs_data:
            paragraph = RectorMessageParagraph.objects.create(
                rector_message=rector,
                order=para_data['order'],
                content=para_data['content'],
                is_active=True
            )
            self.stdout.write(f'  ✅ Created paragraph {para_data["order"] + 1}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Sample data created successfully!'))
        
        # Show summary
        self.stdout.write('\n📊 Summary:')
        self.stdout.write(f'  Featured Sections: {FeaturedSection.objects.filter(is_active=True).count()}')
        self.stdout.write(f'  Active Rectors: {RectorMessage.objects.filter(is_active=True).count()}')
        self.stdout.write(f'  Total Paragraphs: {RectorMessageParagraph.objects.filter(is_active=True).count()}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ You can now test the API!'))
        self.stdout.write('Run: python manage.py debug_rector')
        self.stdout.write('Test URL: http://localhost:8000/about/api/featured/complete/')