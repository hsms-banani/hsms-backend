# academics/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Q, Count
from datetime import date, datetime, timedelta
from calendar import monthrange
import calendar

from .models import (
    # Your existing models
    FacultyMember, Professor, CourseDescription, ResearchPaper, Thesis,
    # New models
    AcademicYear, EventCategory, CalendarEvent, CalendarSettings
)
from .serializers import (
    # Your existing serializers
    FacultyMemberSerializer, ProfessorSerializer, CourseDescriptionSerializer,
    ResearchPaperSerializer, ThesisSerializer,
    # New serializers
    AcademicYearSerializer, EventCategorySerializer, CalendarEventListSerializer,
    CalendarEventDetailSerializer, CalendarEventCreateUpdateSerializer,
    CalendarSettingsSerializer, UpcomingEventsSerializer, MonthlyCalendarSerializer
)

class FacultyMemberList(generics.ListAPIView):
    queryset = FacultyMember.objects.all()
    serializer_class = FacultyMemberSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class FacultyMemberDetail(generics.RetrieveAPIView):
    queryset = FacultyMember.objects.all()
    serializer_class = FacultyMemberSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ProfessorList(generics.ListAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ProfessorDetail(generics.RetrieveAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CourseDescriptionList(generics.ListAPIView):
    queryset = CourseDescription.objects.all()
    serializer_class = CourseDescriptionSerializer

class CourseDescriptionDetail(generics.RetrieveAPIView):
    queryset = CourseDescription.objects.all()
    serializer_class = CourseDescriptionSerializer

class ResearchPaperList(generics.ListAPIView):
    queryset = ResearchPaper.objects.all()
    serializer_class = ResearchPaperSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ResearchPaperDetail(generics.RetrieveAPIView):
    queryset = ResearchPaper.objects.all()
    serializer_class = ResearchPaperSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ThesisList(generics.ListAPIView):
    queryset = Thesis.objects.all()
    serializer_class = ThesisSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ThesisDetail(generics.RetrieveAPIView):
    queryset = Thesis.objects.all()
    serializer_class = ThesisSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

class CalendarEventPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class AcademicYearListView(generics.ListAPIView):
    queryset = AcademicYear.objects.filter(is_active=True)
    serializer_class = AcademicYearSerializer

class AcademicYearDetailView(generics.RetrieveAPIView):
    queryset = AcademicYear.objects.filter(is_active=True)
    serializer_class = AcademicYearSerializer

class EventCategoryListView(generics.ListAPIView):
    queryset = EventCategory.objects.filter(is_active=True)
    serializer_class = EventCategorySerializer

class CalendarEventListView(generics.ListAPIView):
    serializer_class = CalendarEventListSerializer
    pagination_class = CalendarEventPagination

    def get_queryset(self):
        queryset = CalendarEvent.objects.filter(is_published=True).select_related(
            'category', 'academic_year'
        )
        
        # Filter by academic year
        academic_year = self.request.query_params.get('academic_year')
        if academic_year:
            queryset = queryset.filter(academic_year_id=academic_year)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by event type
        event_type = self.request.query_params.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        
        # Filter by month and year
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if month and year:
            queryset = queryset.filter(
                start_date__year=year,
                start_date__month=month
            )
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by time period
        time_filter = self.request.query_params.get('time_filter')
        today = date.today()
        
        if time_filter == 'upcoming':
            queryset = queryset.filter(start_date__gte=today)
        elif time_filter == 'past':
            queryset = queryset.filter(end_date__lt=today)
        elif time_filter == 'current':
            queryset = queryset.filter(
                start_date__lte=today,
                end_date__gte=today
            )
        elif time_filter == 'this_week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            queryset = queryset.filter(
                start_date__gte=week_start,
                start_date__lte=week_end
            )
        elif time_filter == 'this_month':
            queryset = queryset.filter(
                start_date__year=today.year,
                start_date__month=today.month
            )
        elif time_filter == 'next_month':
            if today.month == 12:
                next_month = 1
                next_year = today.year + 1
            else:
                next_month = today.month + 1
                next_year = today.year
            queryset = queryset.filter(
                start_date__year=next_year,
                start_date__month=next_month
            )
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        
        # Filter featured events
        featured = self.request.query_params.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Order by
        order_by = self.request.query_params.get('order_by', 'start_date')
        if order_by in ['start_date', '-start_date', 'title', '-title', 'priority', '-priority']:
            queryset = queryset.order_by(order_by)
        
        return queryset

class CalendarEventDetailView(generics.RetrieveAPIView):
    queryset = CalendarEvent.objects.filter(is_published=True)
    serializer_class = CalendarEventDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CalendarEventCreateView(generics.CreateAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventCreateUpdateSerializer

    def perform_create(self, serializer):
        # You can add authentication here if needed
        serializer.save(created_by=getattr(self.request.user, 'username', 'anonymous'))

class CalendarEventUpdateView(generics.UpdateAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventCreateUpdateSerializer

class CalendarEventDeleteView(generics.DestroyAPIView):
    queryset = CalendarEvent.objects.all()

@api_view(['GET'])
def upcoming_events(request):
    """Get upcoming events for dashboard/widget"""
    limit = int(request.query_params.get('limit', 5))
    days_ahead = int(request.query_params.get('days_ahead', 30))
    
    today = date.today()
    end_date = today + timedelta(days=days_ahead)
    
    events = CalendarEvent.objects.filter(
        is_published=True,
        start_date__gte=today,
        start_date__lte=end_date
    ).select_related('category').order_by('start_date', 'start_time')[:limit]
    
    serializer = UpcomingEventsSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def current_events(request):
    """Get currently happening events"""
    today = date.today()
    
    events = CalendarEvent.objects.filter(
        is_published=True,
        start_date__lte=today,
        end_date__gte=today
    ).select_related('category', 'academic_year').order_by('start_date')
    
    serializer = CalendarEventListSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def monthly_calendar(request, year, month):
    """Get events for a specific month in calendar format"""
    try:
        year = int(year)
        month = int(month)
        
        # Get first and last day of the month
        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])
        
        # Get events for the month
        events = CalendarEvent.objects.filter(
            is_published=True,
            start_date__lte=last_day,
            end_date__gte=first_day
        ).select_related('category').order_by('start_date', 'start_time')
        
        serializer = MonthlyCalendarSerializer(events, many=True)
        
        # Get calendar structure
        cal = calendar.monthcalendar(year, month)
        
        return Response({
            'year': year,
            'month': month,
            'month_name': calendar.month_name[month],
            'calendar_grid': cal,
            'events': serializer.data,
            'first_day': first_day,
            'last_day': last_day
        })
    
    except ValueError:
        return Response(
            {'error': 'Invalid year or month'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def events_by_category(request):
    """Get events grouped by category"""
    academic_year = request.query_params.get('academic_year')
    
    queryset = CalendarEvent.objects.filter(is_published=True)
    if academic_year:
        queryset = queryset.filter(academic_year_id=academic_year)
    
    # Group events by category
    categories = EventCategory.objects.filter(is_active=True).prefetch_related(
        'events'
    ).annotate(
        events_count=Count('events', filter=Q(events__is_published=True))
    )
    
    result = []
    for category in categories:
        category_events = queryset.filter(category=category).order_by('start_date')
        result.append({
            'category': EventCategorySerializer(category).data,
            'events': CalendarEventListSerializer(category_events, many=True).data
        })
    
    return Response(result)

@api_view(['GET'])
def event_statistics(request):
    """Get statistics about events"""
    academic_year = request.query_params.get('academic_year')
    
    queryset = CalendarEvent.objects.filter(is_published=True)
    if academic_year:
        queryset = queryset.filter(academic_year_id=academic_year)
    
    today = date.today()
    
    stats = {
        'total_events': queryset.count(),
        'past_events': queryset.filter(end_date__lt=today).count(),
        'current_events': queryset.filter(
            start_date__lte=today, 
            end_date__gte=today
        ).count(),
        'upcoming_events': queryset.filter(start_date__gt=today).count(),
        'featured_events': queryset.filter(is_featured=True).count(),
        'events_by_type': {},
        'events_by_priority': {},
        'events_by_month': {}
    }
    
    # Events by type
    for event_type, _ in CalendarEvent.EVENT_TYPES:
        count = queryset.filter(event_type=event_type).count()
        if count > 0:
            stats['events_by_type'][event_type] = count
    
    # Events by priority
    for priority, _ in CalendarEvent.PRIORITY_CHOICES:
        count = queryset.filter(priority=priority).count()
        if count > 0:
            stats['events_by_priority'][priority] = count
    
    # Events by month (current year)
    current_year = today.year
    for month in range(1, 13):
        count = queryset.filter(
            start_date__year=current_year,
            start_date__month=month
        ).count()
        if count > 0:
            stats['events_by_month'][calendar.month_name[month]] = count
    
    return Response(stats)

@api_view(['GET'])
def calendar_settings(request):
    """Get calendar settings"""
    try:
        settings = CalendarSettings.objects.first()
        if settings:
            serializer = CalendarSettingsSerializer(settings)
            return Response(serializer.data)
        else:
            # Return default settings if none exist
            return Response({
                'default_academic_year': None,
                'show_weekends': True,
                'default_view': 'month',
                'events_per_page': 10,
                'allow_public_view': True
            })
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def search_events(request):
    """Advanced search for events"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({'results': []})
    
    events = CalendarEvent.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(location__icontains=query) |
        Q(event_type__icontains=query),
        is_published=True
    ).select_related('category', 'academic_year').order_by('start_date')[:20]
    
    serializer = CalendarEventListSerializer(events, many=True)
    return Response({
        'query': query,
        'count': events.count(),
        'results': serializer.data
    })

@api_view(['GET'])
def events_feed(request):
    """RSS-like feed for events"""
    format_type = request.query_params.get('format', 'json')  # json, ical
    limit = int(request.query_params.get('limit', 50))
    
    events = CalendarEvent.objects.filter(
        is_published=True,
        start_date__gte=date.today()
    ).select_related('category', 'academic_year').order_by('start_date')[:limit]
    
    if format_type == 'json':
        serializer = CalendarEventListSerializer(events, many=True)
        return Response({
            'title': 'Academic Calendar Events',
            'description': 'Upcoming academic events',
            'updated': timezone.now(),
            'events': serializer.data
        })
    
    # For iCal format, you would need to implement iCal generation
    # This is a placeholder for future implementation
    return Response({'error': 'iCal format not yet implemented'}, 
                   status=status.HTTP_501_NOT_IMPLEMENTED)