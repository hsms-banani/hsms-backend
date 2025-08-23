# seminary/management/commands/create_history_pages.py
from django.core.management.base import BaseCommand
from seminary.models import Page

class Command(BaseCommand):
    help = 'Create initial History & Heritage pages with content'

    def handle(self, *args, **options):
        pages = [
            {
                'title': 'History & Heritage',
                'slug': 'history-heritage',
                'content': '''
                <div class="prose max-w-none">
                    <p class="lead text-xl text-gray-600 mb-8">Explore the rich history and heritage of the Catholic Church, Bangladesh, and our local Church community.</p>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
                        <div class="text-center bg-white p-8 rounded-lg shadow-lg hover-lift">
                            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <i class="fas fa-church text-4xl text-blue-600"></i>
                            </div>
                            <h3 class="text-2xl font-semibold mb-4 font-serif">Church History</h3>
                            <p class="text-gray-600 leading-relaxed">Discover the 2000-year journey of the Catholic Church from apostolic times to the present day, tracing the development of doctrine, traditions, and global expansion.</p>
                            <a href="/history-heritage/church-history/" class="inline-block mt-4 bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition-colors">Learn More</a>
                        </div>
                        
                        <div class="text-center bg-white p-8 rounded-lg shadow-lg hover-lift">
                            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <i class="fas fa-flag text-4xl text-green-600"></i>
                            </div>
                            <h3 class="text-2xl font-semibold mb-4 font-serif">Bangladesh History</h3>
                            <p class="text-gray-600 leading-relaxed">Learn about the rich cultural and religious heritage of Bangladesh, from ancient civilizations to the modern nation, and its diverse spiritual traditions.</p>
                            <a href="/history-heritage/bangladesh-history/" class="inline-block mt-4 bg-green-600 text-white px-6 py-2 rounded-full hover:bg-green-700 transition-colors">Explore</a>
                        </div>
                        
                        <div class="text-center bg-white p-8 rounded-lg shadow-lg hover-lift">
                            <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <i class="fas fa-home text-4xl text-red-600"></i>
                            </div>
                            <h3 class="text-2xl font-semibold mb-4 font-serif">Local Church History</h3>
                            <p class="text-gray-600 leading-relaxed">Explore the history of the Catholic Church in Bangladesh, from the first missionaries to the establishment of our seminary and local diocese.</p>
                            <a href="/history-heritage/local-church-history/" class="inline-block mt-4 bg-red-600 text-white px-6 py-2 rounded-full hover:bg-red-700 transition-colors">Discover</a>
                        </div>
                    </div>
                </div>
                ''',
                'show_in_menu': True,
                'order': 1
            },
            {
                'title': 'Brief History of the Church',
                'slug': 'church-history',
                'content': '''
                <div class="prose max-w-none">
                    <div class="bg-blue-50 p-8 rounded-lg mb-8">
                        <h2 class="text-3xl font-bold text-blue-800 mb-4 font-serif">The Catholic Church: A 2000-Year Journey</h2>
                        <p class="text-lg text-blue-700">From a small group of disciples in Jerusalem to a global faith community of over 1.3 billion believers worldwide.</p>
                    </div>
                    
                    <div class="timeline space-y-12">
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Apostolic Era (33-100 AD)</h3>
                            <p class="mb-4">The Catholic Church traces its origins to Jesus Christ and the Apostles. After Christ's death and resurrection, the Apostles spread the Gospel throughout the Roman Empire, establishing Christian communities in major cities.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Pentecost (33 AD) - Birth of the Church</li>
                                <li>Council of Jerusalem (49 AD) - First Church council</li>
                                <li>Martyrdom of Peter and Paul in Rome</li>
                                <li>Writing of the New Testament</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Early Church Period (100-313 AD)</h3>
                            <p class="mb-4">Despite severe persecution under various Roman emperors, Christianity continued to grow rapidly. The Church developed its organizational structure, with bishops leading local communities and the Bishop of Rome emerging as a central authority.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Apostolic Fathers and early Christian writings</li>
                                <li>Diocletian Persecution (303-311 AD)</li>
                                <li>Development of episcopal structure</li>
                                <li>Formation of the biblical canon</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Constantine and Legalization (313-476 AD)</h3>
                            <p class="mb-4">Emperor Constantine's Edict of Milan in 313 AD legalized Christianity, leading to rapid expansion throughout the Roman Empire. The first ecumenical councils addressed key theological questions and established fundamental Christian doctrines.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Edict of Milan (313 AD) - Religious freedom</li>
                                <li>Council of Nicaea (325 AD) - Nicene Creed</li>
                                <li>Council of Constantinople (381 AD)</li>
                                <li>Council of Ephesus (431 AD) and Chalcedon (451 AD)</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Medieval Period (476-1453 AD)</h3>
                            <p class="mb-4">The Church became a dominant force in European society, establishing universities, hospitals, and monasteries. This period saw both great achievements and significant challenges, including the Great Schism between East and West.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Rise of monasticism (St. Benedict, St. Francis)</li>
                                <li>Carolingian Renaissance</li>
                                <li>Great Schism of 1054 (East-West split)</li>
                                <li>Crusades (1095-1291)</li>
                                <li>Scholastic theology (St. Thomas Aquinas)</li>
                                <li>Western Schism (1378-1417)</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Reformation and Counter-Reformation (1517-1648)</h3>
                            <p class="mb-4">The Protestant Reformation challenged Church authority and doctrine, leading to the Catholic Counter-Reformation. The Council of Trent clarified Catholic doctrine and initiated significant reforms in Church practices.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Martin Luther's 95 Theses (1517)</li>
                                <li>Council of Trent (1545-1563)</li>
                                <li>Formation of new religious orders (Jesuits)</li>
                                <li>Catholic missions to the Americas and Asia</li>
                                <li>Baroque art and architecture</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Modern Era (1648-Present)</h3>
                            <p class="mb-4">The Church has navigated challenges including the Enlightenment, secularization, and two world wars. The Second Vatican Council brought significant liturgical and pastoral reforms, opening the Church to dialogue with the modern world.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>First Vatican Council (1869-1870) - Papal infallibility</li>
                                <li>Catholic social teaching development</li>
                                <li>Second Vatican Council (1962-1965)</li>
                                <li>Liturgical reforms and vernacular Mass</li>
                                <li>New evangelization efforts</li>
                                <li>Interfaith dialogue initiatives</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="bg-gray-50 p-8 rounded-lg mt-12">
                        <h3 class="text-2xl font-bold mb-4">The Church Today</h3>
                        <p class="text-gray-700 leading-relaxed">Today, the Catholic Church continues its mission of evangelization, education, and service to humanity. With over 1.3 billion members worldwide, it remains the largest Christian denomination, serving communities through parishes, schools, hospitals, and charitable organizations in every corner of the globe.</p>
                    </div>
                </div>
                ''',
                'show_in_menu': False,
                'order': 2
            },
            {
                'title': 'History of Bangladesh',
                'slug': 'bangladesh-history',
                'content': '''
                <div class="prose max-w-none">
                    <div class="bg-green-50 p-8 rounded-lg mb-8">
                        <h2 class="text-3xl font-bold text-green-800 mb-4 font-serif">Bangladesh: Land of Rivers and Rich Heritage</h2>
                        <p class="text-lg text-green-700">A journey through the millennia of Bengal's rich cultural, religious, and political history.</p>
                    </div>
                    
                    <div class="timeline space-y-12">
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Ancient Period (Before 1200 AD)</h3>
                            <p class="mb-4">The region now known as Bangladesh has been inhabited for over 20,000 years. Ancient kingdoms like Gangaridai, Samatata, and Kamarupa flourished here, with Buddhism and Hinduism shaping early culture and civilization.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Stone Age settlements in Chittagong hills</li>
                                <li>Mauryan Empire influence (3rd century BC)</li>
                                <li>Gupta Empire golden age (4th-6th century AD)</li>
                                <li>Pala Empire - Buddhist renaissance (8th-12th century)</li>
                                <li>Sena Dynasty - Hindu revival (11th-12th century)</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Medieval Period (1200-1576 AD)</h3>
                            <p class="mb-4">The arrival of Islam in the 12th century brought significant changes to Bengali society. The Bengal Sultanate emerged as a major independent kingdom, fostering trade, literature, and distinctive Indo-Islamic architecture.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Delhi Sultanate conquest (1204 AD)</li>
                                <li>Bengal Sultanate independence (1352-1576)</li>
                                <li>Development of Bengali language and literature</li>
                                <li>Islamic architecture and mosque building</li>
                                <li>Sufi missionary activities</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Mughal Rule (1576-1757 AD)</h3>
                            <p class="mb-4">Under the Mughal Empire, Bengal became one of the richest provinces. The region was renowned for its textile industry, particularly muslin and silk, which were exported worldwide through European trading companies.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Akbar's conquest of Bengal (1576)</li>
                                <li>Dhaka established as provincial capital (1608)</li>
                                <li>Golden age of Bengali culture and trade</li>
                                <li>European trading posts established</li>
                                <li>Religious syncretism and tolerance</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">British Colonial Period (1757-1947)</h3>
                            <p class="mb-4">The British East India Company's victory at the Battle of Plassey marked the beginning of colonial rule. This period saw economic exploitation, cultural suppression, but also the emergence of Bengali renaissance and freedom movements.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Battle of Plassey (1757) and colonial control</li>
                                <li>Great Bengal Famine (1770)</li>
                                <li>Bengal Renaissance (19th century)</li>
                                <li>Partition of Bengal (1905)</li>
                                <li>Khilafat and Non-cooperation movements</li>
                                <li>Bengal Famine (1943)</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Pakistan Period (1947-1971)</h3>
                            <p class="mb-4">Following the partition of India, East Bengal became East Pakistan. Growing economic disparity, cultural suppression, and political marginalization led to rising nationalism and eventually the Liberation War.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Partition and creation of East Pakistan (1947)</li>
                                <li>Language Movement (1952) - Recognition of Bengali</li>
                                <li>Economic discrimination and neglect</li>
                                <li>Six Point Movement (1966)</li>
                                <li>1970 elections and political crisis</li>
                                <li>Operation Searchlight (March 25, 1971)</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Liberation War and Independence (1971)</h3>
                            <p class="mb-4">After a nine-month Liberation War marked by great sacrifice and international support, Bangladesh gained independence on December 16, 1971, under the leadership of Sheikh Mujibur Rahman.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Declaration of Independence (March 26, 1971)</li>
                                <li>Formation of Mujibnagar Government</li>
                                <li>Guerrilla warfare by Mukti Bahini</li>
                                <li>Indo-Pakistani War (December 1971)</li>
                                <li>Victory Day (December 16, 1971)</li>
                                <li>International recognition</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Modern Bangladesh (1971-Present)</h3>
                            <p class="mb-4">Independent Bangladesh has faced challenges including political instability, natural disasters, and poverty. However, the country has made remarkable progress in economic development, education, healthcare, and women's empowerment.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Constitution adoption (1972)</li>
                                <li>Economic growth and industrialization</li>
                                <li>Garment industry development</li>
                                <li>Microcredit and rural development</li>
                                <li>Digital Bangladesh initiatives</li>
                                <li>Climate change adaptation efforts</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="bg-gray-50 p-8 rounded-lg mt-12">
                        <h3 class="text-2xl font-bold mb-4">Bangladesh Today</h3>
                        <p class="text-gray-700 leading-relaxed">Modern Bangladesh is a proud nation that has preserved its rich cultural heritage while embracing progress. From its ancient roots through colonial struggles to independence and beyond, Bangladesh continues to be known for its resilient people, rich literature, vibrant arts, and strong community bonds that transcend religious and ethnic boundaries.</p>
                    </div>
                </div>
                ''',
                'show_in_menu': False,
                'order': 3
            },
            {
                'title': 'Local Church History',
                'slug': 'local-church-history',
                'content': '''
                <div class="prose max-w-none">
                    <div class="bg-red-50 p-8 rounded-lg mb-8">
                        <h2 class="text-3xl font-bold text-red-800 mb-4 font-serif">The Catholic Church in Bangladesh</h2>
                        <p class="text-lg text-red-700">From the first missionaries to a thriving local Church serving over 350,000 Catholics nationwide.</p>
                    </div>
                    
                    <div class="timeline space-y-12">
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Early Christianity in Bengal (1599-1700)</h3>
                            <p class="mb-4">Christianity first arrived in Bengal through Portuguese traders and missionaries. The first Catholic mission was established in Chittagong in 1599, marking the beginning of organized Christian presence in the region.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Portuguese traders arrive in Chittagong (1599)</li>
                                <li>First Catholic church built in Chittagong</li>
                                <li>Augustinian missionaries begin evangelization</li>
                                <li>Jesuit missions established in Dhaka</li>
                                <li>Early Christian communities formed</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Challenges and Persecutions (1700-1850)</h3>
                            <p class="mb-4">The Church faced various challenges including persecution under Mughal rulers, natural disasters, and conflicts with local authorities. Many early Christians suffered for their faith, yet communities persevered.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Persecution under Mughal authorities</li>
                                <li>Churches destroyed and rebuilt</li>
                                <li>Underground Christian practices</li>
                                <li>Missionary martyrdoms</li>
                                <li>Preservation of faith through oral traditions</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">British Colonial Era and Stability (1850-1947)</h3>
                            <p class="mb-4">Under British rule, the Church gained more stability and protection. Foreign missionary societies, including the Holy Cross Congregation, began systematic evangelization and established schools and hospitals.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Holy Cross Fathers arrive (1853)</li>
                                <li>St. Gregory's High School established (1882)</li>
                                <li>First indigenous priests ordained</li>
                                <li>Catholic hospitals and dispensaries opened</li>
                                <li>Educational missions expanded</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Establishment of Church Hierarchy (1886-1967)</h3>
                            <p class="mb-4">The formal Church hierarchy was established with the creation of the Apostolic Prefecture, later becoming the Diocese of Dacca. This period saw significant growth in both clergy and lay faithful.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Apostolic Prefecture of East Bengal (1886)</li>
                                <li>Diocese of Dacca established (1927)</li>
                                <li>First indigenous bishop ordained (1967)</li>
                                <li>Seminary training programs developed</li>
                                <li>Local religious congregations founded</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Post-Independence Growth (1971-Present)</h3>
                            <p class="mb-4">After Bangladesh's independence, the Church has experienced remarkable growth. Today, there are 8 dioceses serving over 350,000 Catholics, with a strong emphasis on social justice, education, and interfaith dialogue.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Church's role during Liberation War (1971)</li>
                                <li>Establishment of 8 dioceses</li>
                                <li>Growth to over 350,000 Catholics</li>
                                <li>Caritas Bangladesh social programs</li>
                                <li>Interfaith dialogue initiatives</li>
                                <li>Indigenous clergy development</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Holy Spirit Major Seminary</h3>
                            <p class="mb-4">Our seminary represents the commitment to developing indigenous Church leadership. Established to train local clergy who understand and serve the Bangladeshi context, it has been instrumental in the Church's growth and inculturation.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>Founded to train indigenous priests</li>
                                <li>Philosophy and Theology departments</li>
                                <li>Focus on inculturation and local context</li>
                                <li>Academic excellence and spiritual formation</li>
                                <li>Graduates serving nationwide</li>
                                <li>Contribution to local Church leadership</li>
                            </ul>
                        </div>
                        
                        <div class="timeline-item">
                            <h3 class="text-2xl font-bold text-gray-800 mb-4">Current Mission and Future</h3>
                            <p class="mb-4">The Catholic Church in Bangladesh today focuses on education, healthcare, social development, and interfaith dialogue while maintaining its spiritual mission. The Church serves all communities regardless of faith background.</p>
                            <ul class="list-disc list-inside space-y-2 text-gray-700">
                                <li>700+ educational institutions</li>
                                <li>Healthcare services nationwide</li>
                                <li>Social development programs</li>
                                <li>Environmental conservation efforts</li>
                                <li>Youth and family ministries</li>
                                <li>Interfaith harmony promotion</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="bg-gray-50 p-8 rounded-lg mt-12">
                        <h3 class="text-2xl font-bold mb-4">A Living Heritage</h3>
                        <p class="text-gray-700 leading-relaxed">The Catholic Church in Bangladesh continues to be a beacon of hope, service, and faith. From humble beginnings with Portuguese missionaries to a thriving indigenous Church, our history reflects God's providence and the dedication of countless believers who have kept the faith alive through centuries of challenges and triumphs.</p>
                    </div>
                </div>
                ''',
                'show_in_menu': False,
                'order': 4
            }
        ]

        for page_data in pages:
            page, created = Page.objects.get_or_create(
                slug=page_data['slug'],
                defaults=page_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created page: {page.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Page already exists: {page.title}')
                )

        self.stdout.write(
            self.style.SUCCESS('History & Heritage pages creation completed!')
        )