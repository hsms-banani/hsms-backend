# Create this file: seminary/management/commands/create_seminary_pages.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from seminary.models import Page, SiteSettings

class Command(BaseCommand):
    help = 'Create default pages for Holy Spirit Major Seminary'

    def handle(self, *args, **options):
        # Create or update site settings
        site_settings, created = SiteSettings.objects.get_or_create(
            id=1,
            defaults={
                'site_name': 'Holy Spirit Major Seminary',
                'site_motto': 'Dedicated for Service',
                'address': 'Holy Spirit Major Seminary\nDhaka, Bangladesh',
                'phone': '+880-2-XXXXXXXX',
                'email': 'info@hsms.edu.bd',
                'facebook_url': 'https://facebook.com/hsms.bd',
                'meta_description': 'Holy Spirit Major Seminary - Dedicated for Service. A Catholic seminary in Bangladesh providing philosophical and theological education.',
                'meta_keywords': 'seminary, theology, philosophy, catholic, bangladesh, education, priestly formation'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created site settings'))

        pages_data = [
            {
                'title': 'Rector\'s Welcome',
                'slug': 'rector-welcome',
                'content': '''
<div class="rector-welcome">
    <h2>Welcome to Holy Spirit Major Seminary</h2>
    
    <div class="rector-message">
        <p>Dear Friends and Visitors,</p>
        
        <p>It is my great pleasure to welcome you to the Holy Spirit Major Seminary, an institution dedicated to the formation of future priests for the Catholic Church in Bangladesh and beyond.</p>
        
        <p>Our seminary stands as a beacon of hope and spiritual formation, where young men discern their calling to serve God and His people. For decades, we have been committed to providing comprehensive philosophical and theological education, combined with spiritual, pastoral, and human formation.</p>
        
        <p>At Holy Spirit Major Seminary, we believe in nurturing not just the intellectual capabilities of our seminarians, but also their spiritual depth, pastoral sensitivity, and human maturity. Our faculty, consisting of dedicated priests and lay professionals, work tirelessly to ensure that each seminarian receives the best possible formation.</p>
        
        <p>Our beautiful campus provides an environment conducive to prayer, study, and community life. Here, seminarians from different dioceses and religious congregations come together to form a vibrant community of faith and learning.</p>
        
        <p>We are proud of our alumni who now serve as priests in parishes, schools, hospitals, and various ministries across Bangladesh and in other countries. They carry with them the values and formation they received at our seminary.</p>
        
        <p>Whether you are considering a vocation to the priesthood, seeking spiritual guidance, or simply interested in learning about our work, we welcome you with open arms. Please feel free to visit us, participate in our programs, or contact us for any assistance.</p>
        
        <p>May the Holy Spirit, our patron, continue to guide and bless our seminary and all who are part of our community.</p>
        
        <p>In Christ,<br>
        <strong>Fr. [Rector's Name]</strong><br>
        Rector, Holy Spirit Major Seminary</p>
    </div>
</div>
                ''',
                'meta_description': 'Welcome message from the Rector of Holy Spirit Major Seminary, highlighting our mission of priestly formation and spiritual education.',
                'is_published': True,
                'show_in_menu': True,
                'order': 1
            },
            {
                'title': 'Mission and Vision',
                'slug': 'mission-vision',
                'content': '''
<div class="mission-vision">
    <div class="vision-section">
        <h2>Our Vision</h2>
        <p>To be a leading institution in priestly formation, preparing holy and competent priests who will serve the Church and society with dedication, integrity, and pastoral charity.</p>
    </div>
    
    <div class="mission-section">
        <h2>Our Mission</h2>
        <p>Holy Spirit Major Seminary is committed to:</p>
        <ul>
            <li>Providing comprehensive philosophical and theological education based on the teachings of the Catholic Church</li>
            <li>Fostering spiritual formation rooted in prayer, sacramental life, and personal relationship with Jesus Christ</li>
            <li>Developing pastoral skills and missionary zeal for effective ministry</li>
            <li>Promoting intellectual growth and critical thinking</li>
            <li>Building character and human maturity essential for priestly life</li>
            <li>Encouraging cultural sensitivity and inculturation in ministry</li>
            <li>Preparing priests who are servants of the Gospel and advocates for social justice</li>
        </ul>
    </div>
    
    <div class="values-section">
        <h2>Our Core Values</h2>
        <div class="values-grid">
            <div class="value-item">
                <h3>Holiness</h3>
                <p>Striving for personal sanctification and helping others in their spiritual journey</p>
            </div>
            <div class="value-item">
                <h3>Service</h3>
                <p>Dedicated service to God, Church, and humanity, especially the poor and marginalized</p>
            </div>
            <div class="value-item">
                <h3>Excellence</h3>
                <p>Pursuing academic and pastoral excellence in all endeavors</p>
            </div>
            <div class="value-item">
                <h3>Community</h3>
                <p>Building fraternal relationships and fostering unity in diversity</p>
            </div>
            <div class="value-item">
                <h3>Truth</h3>
                <p>Commitment to seeking and proclaiming the truth of the Gospel</p>
            </div>
            <div class="value-item">
                <h3>Compassion</h3>
                <p>Showing Christ's love and mercy to all people, regardless of background</p>
            </div>
        </div>
    </div>
</div>
                ''',
                'meta_description': 'Mission, vision, and core values of Holy Spirit Major Seminary - our commitment to priestly formation and service.',
                'is_published': True,
                'show_in_menu': True,
                'order': 2
            },
            {
                'title': 'Seminary History',
                'slug': 'seminary-history',
                'content': '''
<div class="seminary-history">
    <h2>History of Holy Spirit Major Seminary</h2>
    
    <div class="timeline">
        <div class="timeline-item">
            <h3>Foundation Years</h3>
            <p>Holy Spirit Major Seminary was established with the vision of providing quality priestly formation in Bangladesh. The seminary was founded to meet the growing need for well-trained priests in the region.</p>
        </div>
        
        <div class="timeline-item">
            <h3>Early Development</h3>
            <p>In its early years, the seminary focused on building a strong foundation in philosophical studies while developing the spiritual and human formation programs that would become its hallmark.</p>
        </div>
        
        <div class="timeline-item">
            <h3>Expansion and Growth</h3>
            <p>As the seminary grew, additional facilities were added, including a larger library, more classrooms, and improved residential facilities for seminarians. The theology department was established to provide comprehensive theological education.</p>
        </div>
        
        <div class="timeline-item">
            <h3>Academic Recognition</h3>
            <p>The seminary gained recognition for its academic programs and began attracting students not only from Bangladesh but from neighboring countries as well.</p>
        </div>
        
        <div class="timeline-item">
            <h3>Modern Era</h3>
            <p>Today, Holy Spirit Major Seminary stands as one of the premier institutions for priestly formation in South Asia, with modern facilities, qualified faculty, and a comprehensive curriculum that prepares priests for contemporary ministry challenges.</p>
        </div>
    </div>
    
    <div class="heritage-section">
        <h3>Our Heritage</h3>
        <p>Throughout its history, Holy Spirit Major Seminary has maintained its commitment to excellence in priestly formation. Our alumni serve in various capacities across Bangladesh and internationally, carrying forward the values and formation they received here.</p>
        
        <p>The seminary has been blessed with dedicated faculty, supportive bishops, and generous benefactors who have contributed to its growth and development over the years.</p>
    </div>
</div>
                ''',
                'meta_description': 'Learn about the rich history and heritage of Holy Spirit Major Seminary, from its foundation to becoming a premier institution for priestly formation.',
                'is_published': True,
                'show_in_menu': True,
                'order': 3
            },
            {
                'title': 'Formation Program',
                'slug': 'formation-program',
                'content': '''
<div class="formation-program">
    <h2>Priestly Formation Program</h2>
    
    <p>Our comprehensive formation program is designed to prepare seminarians for effective priestly ministry in the modern world. The program encompasses four essential dimensions of formation:</p>
    
    <div class="formation-dimensions">
        <div class="dimension">
            <h3>1. Spiritual Formation</h3>
            <p>The heart of our program focuses on developing a deep personal relationship with Jesus Christ through:</p>
            <ul>
                <li>Daily Eucharistic celebration and adoration</li>
                <li>Regular reception of the Sacrament of Reconciliation</li>
                <li>Liturgy of the Hours (Divine Office)</li>
                <li>Personal prayer and meditation</li>
                <li>Retreats and spiritual direction</li>
                <li>Devotion to the Blessed Virgin Mary</li>
            </ul>
        </div>
        
        <div class="dimension">
            <h3>2. Intellectual Formation</h3>
            <p>Academic excellence is pursued through:</p>
            <ul>
                <li>Two-year Philosophy program</li>
                <li>Four-year Theology program</li>
                <li>Sacred Scripture studies</li>
                <li>Church History and Patristics</li>
                <li>Moral and Dogmatic Theology</li>
                <li>Canon Law</li>
                <li>Liturgical studies</li>
                <li>Pastoral theology and counseling</li>
            </ul>
        </div>
        
        <div class="dimension">
            <h3>3. Pastoral Formation</h3>
            <p>Practical ministry preparation includes:</p>
            <ul>
                <li>Parish ministry experience</li>
                <li>Hospital and institutional chaplaincy</li>
                <li>Youth ministry programs</li>
                <li>Social service projects</li>
                <li>Preaching and homiletics</li>
                <li>Catechetical instruction</li>
                <li>Marriage and family counseling preparation</li>
            </ul>
        </div>
        
        <div class="dimension">
            <h3>4. Human Formation</h3>
            <p>Personal development and character building through:</p>
            <ul>
                <li>Community living and fraternity</li>
                <li>Leadership development</li>
                <li>Communication skills</li>
                <li>Emotional maturity and self-awareness</li>
                <li>Cultural sensitivity and inculturation</li>
                <li>Physical fitness and health</li>
                <li>Arts and recreation</li>
            </ul>
        </div>
    </div>
    
    <div class="program-structure">
        <h3>Program Structure</h3>
        <div class="years-breakdown">
            <div class="year-block">
                <h4>Years 1-2: Philosophy</h4>
                <p>Foundation in philosophical thinking, logic, ethics, and fundamental theology. Focus on human formation and spiritual development.</p>
            </div>
            <div class="year-block">
                <h4>Years 3-6: Theology</h4>
                <p>Comprehensive theological education covering all major areas of Catholic theology, with increasing emphasis on pastoral formation.</p>
            </div>
            <div class="year-block">
                <h4>Pastoral Year</h4>
                <p>Practical ministry experience in parishes or institutions under supervision, applying theological knowledge to pastoral situations.</p>
            </div>
        </div>
    </div>
</div>
                ''',
                'meta_description': 'Comprehensive priestly formation program at Holy Spirit Major Seminary covering spiritual, intellectual, pastoral, and human formation.',
                'is_published': True,
                'show_in_menu': True,
                'order': 4
            },
            {
                'title': 'Rules and Regulations',
                'slug': 'rules-regulations',
                'content': '''
<div class="rules-regulations">
    <h2>Seminary Rules and Regulations</h2>
    
    <div class="intro">
        <p>The following rules and regulations are designed to create an environment conducive to priestly formation and community life. All seminarians are expected to observe these guidelines with maturity and responsibility.</p>
    </div>
    
    <div class="section">
        <h3>Daily Schedule</h3>
        <ul>
            <li>5:30 AM - Rising and personal prayer</li>
            <li>6:00 AM - Lauds (Morning Prayer)</li>
            <li>6:30 AM - Holy Mass</li>
            <li>7:30 AM - Breakfast</li>
            <li>8:30 AM - 12:00 PM - Classes</li>
            <li>12:00 PM - Angelus and lunch</li>
            <li>1:00 PM - 2:00 PM - Rest/Siesta</li>
            <li>2:00 PM - 5:00 PM - Study/Classes</li>
            <li>5:00 PM - Recreation/Sports</li>
            <li>6:00 PM - Vespers (Evening Prayer)</li>
            <li>7:00 PM - Dinner</li>
            <li>8:00 PM - Community time/Study</li>
            <li>9:00 PM - Compline</li>
            <li>10:00 PM - Lights out</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>Academic Requirements</h3>
        <ul>
            <li>Regular attendance at all classes is mandatory</li>
            <li>Minimum 75% attendance required for examinations</li>
            <li>Assignments must be submitted on time</li>
            <li>Plagiarism is strictly prohibited</li>
            <li>Academic honesty is expected in all examinations</li>
            <li>Study hours must be observed in silence</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>Spiritual Life</h3>
        <ul>
            <li>Participation in daily Mass is obligatory</li>
            <li>Weekly confession is encouraged</li>
            <li>Monthly spiritual direction meetings are required</li>
            <li>Annual retreats are mandatory</li>
            <li>Proper reverence in chapel at all times</li>
            <li>Sacred space to be maintained in silence</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>Community Life</h3>
        <ul>
            <li>Respect for all community members</li>
            <li>Participation in community activities</li>
            <li>Care for common property</li>
            <li>Cleanliness of personal and common areas</li>
            <li>Proper dress code at all times</li>
            <li>Meals taken in common unless excused</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>Communication and Technology</h3>
        <ul>
            <li>Use of mobile phones restricted during study and prayer times</li>
            <li>Internet usage monitored and regulated</li>
            <li>Social media use should reflect seminary values</li>
            <li>Permission required for external communications</li>
            <li>Visiting hours for family and friends are specified</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>Leave and Permissions</h3>
        <ul>
            <li>Permission required for leaving seminary premises</li>
            <li>Home visits during scheduled vacation periods</li>
            <li>Medical appointments with proper authorization</li>
            <li>Emergency leave with rector's approval</li>
            <li>Overnight stays require special permission</li>
        </ul>
    </div>
    
    <div class="disciplinary">
        <h3>Disciplinary Measures</h3>
        <p>Violation of seminary rules may result in:</p>
        <ul>
            <li>Verbal warning and counseling</li>
            <li>Written warning</li>
            <li>Temporary suspension</li>
            <li>Dismissal from the seminary</li>
        </ul>
        <p>All disciplinary actions follow due process and provide opportunity for dialogue and improvement.</p>
    </div>
</div>
                ''',
                'meta_description': 'Rules and regulations for seminarians at Holy Spirit Major Seminary governing academic, spiritual, and community life.',
                'is_published': True,
                'show_in_menu': True,
                'order': 5
            }
        ]

        # Create pages
        for page_data in pages_data:
            page, created = Page.objects.get_or_create(
                slug=page_data['slug'],
                defaults=page_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created page: {page_data["title"]}')
                )
            else:
                # Update existing page
                for key, value in page_data.items():
                    setattr(page, key, value)
                page.save()
                self.stdout.write(
                    self.style.WARNING(f'Updated page: {page_data["title"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created/updated seminary pages!')
        )