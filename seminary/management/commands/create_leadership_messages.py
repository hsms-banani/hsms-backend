# Create this file: your_app/management/commands/create_leadership_messages.py
# Run with: python manage.py create_leadership_messages

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from seminary.models import LeadershipMessage, Page

class Command(BaseCommand):
    help = 'Create initial leadership messages from existing pages'
    
    def handle(self, *args, **options):
        # Get or create admin user for author field
        admin_user = User.objects.filter(is_superuser=True).first()
        
        # Create Rector Welcome Message
        rector_message, created = LeadershipMessage.objects.get_or_create(
            message_type='rector',
            defaults={
                'title': 'Welcome from the Rector',
                'leader_name': 'Rev. Fr. [Rector Name]',
                'leader_title': 'Rector, Holy Spirit Major Seminary',
                'message_content': '''
                <h2>Dear Friends and Visitors,</h2>
                
                <p>It is with great joy and enthusiasm that I welcome you to the Holy Spirit Major Seminary. As the Rector of this esteemed institution, I am honored to share with you the rich tradition and vibrant community that defines our seminary.</p>
                
                <p>Our seminary stands as a beacon of spiritual formation, academic excellence, and pastoral preparation. For many years, we have been dedicated to forming men called to serve God and His people through the sacred priesthood. Our mission extends beyond mere academic instruction; we strive to nurture the whole person—intellectually, spiritually, emotionally, and pastorally.</p>
                
                <h3>Our Commitment to Excellence</h3>
                
                <p>At Holy Spirit Major Seminary, we believe that the formation of future priests requires a comprehensive approach that integrates rigorous academic study with deep spiritual growth. Our faculty, comprised of dedicated priests, religious, and lay professionals, brings decades of experience in theology, philosophy, and pastoral ministry.</p>
                
                <p>We offer a challenging curriculum that prepares our seminarians for the complexities of modern ministry while remaining rooted in the timeless traditions of the Catholic Church. Our programs encompass systematic theology, moral theology, Church history, canon law, liturgy, and pastoral theology, all designed to provide a solid foundation for effective ministry.</p>
                
                <h3>Spiritual Formation</h3>
                
                <p>The heart of seminary life is spiritual formation. Through daily Mass, regular prayer, spiritual direction, and retreats, our seminarians develop a deep relationship with Christ that will sustain them throughout their priestly ministry. We emphasize the importance of personal holiness as the foundation of effective pastoral service.</p>
                
                <p>Our beautiful chapel serves as the center of our community life, where we gather daily for prayer and worship. The peaceful atmosphere of our campus provides an ideal environment for reflection, study, and spiritual growth.</p>
                
                <h3>Community Life</h3>
                
                <p>Seminary life is inherently communal. Our seminarians live, study, and pray together, forming lasting bonds that will serve them well in their future ministry. We encourage mutual support, fraternal correction, and collaborative learning as essential elements of priestly formation.</p>
                
                <h3>Looking Forward</h3>
                
                <p>As we continue to serve the Church in the 21st century, we remain committed to adapting our methods while preserving our core mission. We embrace new technologies and pedagogical approaches that enhance learning while maintaining the essential elements of traditional priestly formation.</p>
                
                <p>I invite you to explore our website, visit our campus, and learn more about the great work being done at Holy Spirit Major Seminary. Whether you are a young man discerning a call to the priesthood, a family member supporting someone in formation, or simply someone interested in our mission, you will always find a warm welcome here.</p>
                
                <p>May God bless you abundantly, and may our Blessed Mother, under the title of the Immaculate Conception, intercede for all our needs.</p>
                ''',
                'quote': 'Called to serve, formed to lead, sent to sanctify the People of God.',
                'meta_description': 'Welcome message from the Rector of Holy Spirit Major Seminary',
                'author': admin_user,
                'is_published': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Rector welcome message')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Rector welcome message already exists')
            )
        
        # Create Director Message
        director_message, created = LeadershipMessage.objects.get_or_create(
            message_type='director',
            defaults={
                'title': 'Message from the Director',
                'leader_name': 'Rev. Dr. [Director Name]',
                'leader_title': 'Director, Holy Spirit Institute of Theology',
                'message_content': '''
                <h2>Welcome to the Holy Spirit Institute of Theology (HSIT)</h2>
                
                <p>Greetings and peace in Christ! As the Director of the Holy Spirit Institute of Theology, I am delighted to welcome you to our academic community dedicated to excellence in theological education and research.</p>
                
                <p>HSIT represents the culmination of decades of commitment to providing rigorous theological education that serves both our seminary community and the broader Catholic Church. Our institute stands as a testament to the Church's ongoing commitment to intellectual excellence in the service of faith.</p>
                
                <h3>Academic Excellence</h3>
                
                <p>Our Institute offers comprehensive programs in both Philosophy and Theology, designed to meet the highest academic standards while remaining deeply rooted in the Catholic intellectual tradition. We are proud of our distinguished faculty who bring together pastoral experience, scholarly expertise, and a genuine love for teaching.</p>
                
                <p>Our Philosophy Department provides a solid foundation in the perennial questions of human existence, ethics, and metaphysics. Students engage with both classical and contemporary philosophical thought, developing critical thinking skills essential for theological study and pastoral ministry.</p>
                
                <p>The Theology Department offers a comprehensive curriculum covering all major areas of theological inquiry: systematic theology, moral theology, biblical studies, Church history, liturgical studies, and pastoral theology. Our approach integrates traditional scholastic methodology with contemporary theological insights.</p>
                
                <h3>Research and Scholarship</h3>
                
                <p>HSIT is committed to contributing to the broader theological conversation through research, publications, and scholarly exchange. Our faculty actively engage in research projects that advance our understanding of the faith and address contemporary challenges facing the Church.</p>
                
                <p>We regularly host conferences, seminars, and workshops that bring together scholars, pastors, and students to explore important theological questions. These events foster intellectual dialogue and contribute to the ongoing development of Catholic theology.</p>
                
                <h3>Formation for Service</h3>
                
                <p>While maintaining the highest academic standards, we never lose sight of our primary mission: forming men and women for service to the Church. Our programs are designed not merely to impart knowledge, but to foster wisdom, virtue, and pastoral sensitivity.</p>
                
                <p>We understand that theological education is ultimately about encountering the living God and being transformed by that encounter. Our faculty serve not only as teachers but as mentors and spiritual guides, helping students integrate their academic learning with their spiritual and personal development.</p>
                
                <h3>Library and Resources</h3>
                
                <p>Our well-equipped library serves as the heart of our academic community, housing an extensive collection of theological and philosophical works. We continually expand our resources, including digital databases and online materials, to support cutting-edge research and study.</p>
                
                <h3>Future Vision</h3>
                
                <p>As we look to the future, HSIT remains committed to excellence in theological education while adapting to the evolving needs of the Church. We are exploring new programs, expanding our research capabilities, and seeking new ways to serve the broader Catholic community.</p>
                
                <p>I encourage you to explore what HSIT has to offer, whether you are a prospective student, a fellow educator, or someone simply interested in theological learning. We are here to serve the Church's mission of evangelization through excellence in theological education.</p>
                ''',
                'quote': 'Fides quaerens intellectum - Faith seeking understanding through rigorous theological inquiry.',
                'meta_description': 'Message from the Director of Holy Spirit Institute of Theology',
                'author': admin_user,
                'is_published': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Director message')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Director message already exists')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Leadership messages setup completed!')
        )


            # Create Director Message
        director_message, created = LeadershipMessage.objects.get_or_create(
            message_type='director',
            defaults={
                'title': 'Message from the Director',
                'leader_name': 'Rev. Dr. [Director Name]',
                'leader_title': 'Director, Holy Spirit Institute of Theology',
                'message_content': '''
                <h2>Welcome to the Holy Spirit Institute of Theology (HSIT)</h2>
                
                <p>Greetings and peace in Christ! As the Director of the Holy Spirit Institute of Theology, I am delighted to welcome you to our academic community dedicated to excellence in theological education and research.</p>
                
                <p>HSIT represents the culmination of decades of commitment to providing rigorous theological education that serves both our seminary community and the broader Catholic Church. Our institute stands as a testament to the Church's ongoing commitment to intellectual excellence in the service of faith.</p>
                
                <h3>Academic Excellence</h3>
                
                <p>Our Institute offers comprehensive programs in both Philosophy and Theology, designed to meet the highest academic standards while remaining deeply rooted in the Catholic intellectual tradition. We are proud of our distinguished faculty who bring together pastoral experience, scholarly expertise, and a genuine love for teaching.</p>
                
                <p>Our Philosophy Department provides a solid foundation in the perennial questions of human existence, ethics, and metaphysics. Students engage with both classical and contemporary philosophical thought, developing critical thinking skills essential for theological study and pastoral ministry.</p>
                
                <p>The Theology Department offers a comprehensive curriculum covering all major areas of theological inquiry: systematic theology, moral theology, biblical studies, Church history, liturgical studies, and pastoral theology. Our approach integrates traditional scholastic methodology with contemporary theological insights.</p>
                
                <h3>Research and Scholarship</h3>
                
                <p>HSIT is committed to contributing to the broader theological conversation through research, publications, and scholarly exchange. Our faculty actively engage in research projects that advance our understanding of the faith and address contemporary challenges facing the Church.</p>
                
                <p>We regularly host conferences, seminars, and workshops that bring together scholars, pastors, and students to explore important theological questions. These events foster intellectual dialogue and contribute to the ongoing development of Catholic theology.</p>
                
                <h3>Formation for Service</h3>
                
                <p>While maintaining the highest academic standards, we never lose sight of our primary mission: forming men and women for service to the Church. Our programs are designed not merely to impart knowledge, but to foster wisdom, virtue, and pastoral sensitivity.</p>
                
                <p>We understand that theological education is ultimately about encountering the living God and being transformed by that encounter. Our faculty serve not only as teachers but as mentors and spiritual guides, helping students integrate their academic learning with their spiritual and personal development.</p>
                
                <h3>Library and Resources</h3>
                
                <p>Our well-equipped library serves as the heart of our academic community, housing an extensive collection of theological and philosophical works. We continually expand our resources, including digital databases and online materials, to support cutting-edge research and study.</p>
                
                <h3>Future Vision</h3>
                
                <p>As we look to the future, HSIT remains committed to excellence in theological education while adapting to the evolving needs of the Church. We are exploring new programs, expanding our research capabilities, and seeking new ways to serve the broader Catholic community.</p>
                
                <p>I encourage you to explore what HSIT has to offer, whether you are a prospective student, a fellow educator, or someone simply interested in theological learning. We are here to serve the Church's mission of evangelization through excellence in theological education.</p>
                ''',
                'quote': 'Fides quaerens intellectum - Faith seeking understanding through rigorous theological inquiry.',
                'meta_description': 'Message from the Director of Holy Spirit Institute of Theology',
                'author': admin_user,
                'is_published': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Director message')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Director message already exists')
            )
        
        # Create Spiritual Director Message
        spiritual_director_message, created = LeadershipMessage.objects.get_or_create(
            message_type='spiritual_director',
            defaults={
                'title': "Spiritual Director's Message",
                'leader_name': 'Rev. Fr. [Spiritual Director Name]',
                'leader_title': 'Spiritual Director, Holy Spirit Major Seminary',
                'message_content': '''
                <h2>From the Spiritual Director's Desk</h2>
                
                <p>Dear Brothers and Sisters in Christ, Peace and joy in the Lord! As the Spiritual Director of Holy Spirit Major Seminary, I am privileged to accompany our seminarians on their journey of spiritual formation and discernment.</p>
                
                <p>The path to priesthood is fundamentally a spiritual journey—a response to Christ's call to "come, follow me." It is my sacred responsibility to help guide each seminarian as he discerns God's will and develops the spiritual foundation necessary for effective priestly ministry.</p>
                
                <h3>The Heart of Formation</h3>
                
                <p>Spiritual formation is not merely an aspect of seminary life; it is the very heart that gives life to all other dimensions of priestly preparation. Without a deep, personal relationship with Jesus Christ, academic knowledge remains sterile, and pastoral skills lack the power to transform souls.</p>
                
                <p>In our spiritual formation program, we emphasize four foundational pillars: prayer, sacramental life, spiritual direction, and apostolic service. Each seminarian is encouraged to develop a personal prayer life that will sustain him throughout his years of ministry.</p>
                
                <h3>Prayer as the Foundation</h3>
                
                <p>Prayer is the priest's lifeline to God. We begin each day with Morning Prayer and the celebration of the Eucharist, which forms the center of our community life. Through Adoration of the Blessed Sacrament, the Liturgy of the Hours, and personal meditation, our seminarians learn to find their strength in communion with Christ.</p>
                
                <p>The Rosary holds a special place in our daily rhythm, as we entrust ourselves to the intercession of Our Lady, the Mother of Priests. Mary's "yes" to God serves as a model for every priestly vocation.</p>
                
                <h3>Sacramental Life</h3>
                
                <p>The sacraments are God's gifts of grace, and future priests must be men deeply formed by sacramental life. Regular celebration of the Eucharist, frequent reception of the Sacrament of Reconciliation, and participation in the other sacraments help form our seminarians in holiness.</p>
                
                <p>We place particular emphasis on preparing our men to be worthy celebrants of the sacred mysteries. The way a priest celebrates Mass speaks volumes about his faith and can inspire or discourage the faithful entrusted to his care.</p>
                
                <h3>Spiritual Direction</h3>
                
                <p>Each seminarian meets regularly with a spiritual director who helps him discern God's will, grow in virtue, and address the challenges that arise in formation. This one-on-one mentorship is crucial for healthy spiritual development and honest self-reflection.</p>
                
                <p>Spiritual direction provides a safe space for seminarians to discuss their struggles, celebrate their growth, and receive guidance in their journey toward ordination. It is through this relationship that many of the most important insights and breakthroughs occur.</p>
                
                <h3>Apostolic Service</h3>
                
                <p>A priest is called to serve, not to be served. Our seminarians regularly participate in various apostolic works: visiting the sick, serving in parishes, working with youth, and engaging in works of mercy. These experiences help them develop pastoral hearts and practical ministry skills.</p>
                
                <h3>Challenges and Growth</h3>
                
                <p>The journey to priesthood is not without its challenges. Seminarians face questions about celibacy, struggles with personal weaknesses, and the normal difficulties of human growth. We approach these challenges with patience, understanding, and firm guidance rooted in Church teaching.</p>
                
                <p>Each man's journey is unique, and we respect the individual pace of growth while maintaining high standards for priestly formation. Some may need additional time for maturation, while others may discover that God is calling them to a different vocation.</p>
                
                <h3>A Community of Support</h3>
                
                <p>Spiritual formation happens not in isolation but within a community of faith. Our seminarians support one another through prayer, friendship, and fraternal correction. They learn that priesthood, while requiring personal holiness, is never a solitary endeavor.</p>
                
                <p>The seminary community includes not only seminarians and faculty but also staff, benefactors, and the many faithful who support priestly formation through their prayers and sacrifices.</p>
                
                <h3>Looking Toward Ordination</h3>
                
                <p>As seminarians progress through their formation, they are gradually configured more closely to Christ the High Priest. The minor orders of Lector and Acolyte, followed by the diaconate, mark important milestones in their spiritual journey.</p>
                
                <p>Ordination to the priesthood is not an end but a beginning—the moment when a man is sacramentally configured to Christ in a unique way and sent forth to serve God's people. All of our formation aims toward preparing men for this sacred responsibility.</p>
                
                <h3>A Call to Prayer</h3>
                
                <p>I invite all who visit this page to join us in prayer for vocations to the priesthood. Our Church needs holy priests, and holy priests come from communities that pray for them, support them, and encourage young men to consider this beautiful calling.</p>
                
                <p>Pray especially for our current seminarians, that they may grow in holiness and respond generously to whatever God asks of them. Pray also for their families, who make significant sacrifices to support their sons' discernment.</p>
                
                <h3>Final Thoughts</h3>
                
                <p>The privilege of accompanying men in their formation for priesthood is one of the greatest joys of my own priestly life. To witness young men grow in holiness, develop their gifts, and prepare to serve God's people is to see the Church's future taking shape.</p>
                
                <p>If you are a young man considering a call to priesthood, I encourage you to speak with your pastor, spend time in prayer before the Blessed Sacrament, and consider visiting our seminary. God's call often begins as a whisper, but it grows stronger as we open our hearts to His voice.</p>
                
                <p>May Our Lord continue to bless our seminary, our seminarians, and all those who support the formation of future priests. Together, we participate in Christ's mission of salvation and help ensure that future generations will have holy priests to guide them closer to God.</p>
                ''',
                'quote': 'Come, follow me, and I will make you fishers of men. The call to priesthood is Christ\'s personal invitation to total surrender in service of His people.',
                'meta_description': 'Message from the Spiritual Director of Holy Spirit Major Seminary',
                'author': admin_user,
                'is_published': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Spiritual Director message')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Spiritual Director message already exists')
            )