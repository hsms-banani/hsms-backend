# apps/students/views.py (UPDATED with status filtering)
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from .models import (
    Student, EnrollmentRequirement, ExamInformation,
    TuitionFee, Document, FAQ, SpiritualGuidance
)
from .serializers import (
    StudentSerializer, EnrollmentRequirementSerializer,
    ExamInformationSerializer, TuitionFeeSerializer,
    DocumentSerializer, FAQSerializer, SpiritualGuidanceSerializer
)

@method_decorator(csrf_exempt, name='dispatch')
class StudentList(generics.ListAPIView):
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        # Get status filter (default to 'active' for backward compatibility)
        status = self.request.query_params.get('status', 'active')
        
        # Base queryset with status filtering
        if status == 'all':
            queryset = Student.objects.all().order_by('name')
        else:
            queryset = Student.objects.filter(status=status).order_by('name')
        
        # Additional filters
        congregation = self.request.query_params.get('congregation', None)
        diocese = self.request.query_params.get('diocese', None)
        year_joined = self.request.query_params.get('year_joined', None)
        
        if congregation:
            queryset = queryset.filter(congregation__icontains=congregation)
        if diocese:
            queryset = queryset.filter(diocese__icontains=diocese)
        if year_joined:
            queryset = queryset.filter(year_joined=year_joined)
        
        return queryset

@method_decorator(csrf_exempt, name='dispatch')
class CongregationList(generics.ListAPIView):
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        status = self.request.query_params.get('status', 'active')
        if status == 'all':
            return Student.objects.all()
        else:
            return Student.objects.filter(status=status)
    
    def list(self, request, *args, **kwargs):
        status = self.request.query_params.get('status', 'active')
        
        # Build base queryset
        if status == 'all':
            base_queryset = Student.objects.all()
        else:
            base_queryset = Student.objects.filter(status=status)
        
        # Get congregation and diocese statistics
        congregations = base_queryset.values('congregation').annotate(
            count=Count('id')
        ).order_by('congregation')
        
        dioceses = base_queryset.values('diocese').annotate(
            count=Count('id')
        ).order_by('diocese')
        
        return Response({
            'congregations': list(congregations),
            'dioceses': list(dioceses),
            'total_students': base_queryset.count(),
            'status_filter': status
        })

@method_decorator(csrf_exempt, name='dispatch')
class EnrollmentRequirementList(generics.ListAPIView):
    queryset = EnrollmentRequirement.objects.all().order_by('order', 'title')
    serializer_class = EnrollmentRequirementSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ExamInformationList(generics.ListAPIView):
    queryset = ExamInformation.objects.filter(is_active=True).order_by('-exam_date')
    serializer_class = ExamInformationSerializer

@method_decorator(csrf_exempt, name='dispatch')
class TuitionFeeList(generics.ListAPIView):
    queryset = TuitionFee.objects.filter(is_active=True).order_by('fee_type', 'title')
    serializer_class = TuitionFeeSerializer

@method_decorator(csrf_exempt, name='dispatch')
class DocumentList(generics.ListAPIView):
    serializer_class = DocumentSerializer
    
    def get_queryset(self):
        queryset = Document.objects.all().order_by('category', 'title')
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

@method_decorator(csrf_exempt, name='dispatch')
class FAQList(generics.ListAPIView):
    serializer_class = FAQSerializer
    
    def get_queryset(self):
        queryset = FAQ.objects.all().order_by('category', 'order', 'question')
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

@method_decorator(csrf_exempt, name='dispatch')
class SpiritualGuidanceList(generics.ListAPIView):
    queryset = SpiritualGuidance.objects.all().order_by('-is_featured', '-created_at')
    serializer_class = SpiritualGuidanceSerializer

# Test endpoint
@csrf_exempt
@require_http_methods(["GET"])
def api_test(request):
    """Test endpoint to verify API is working"""
    return JsonResponse({
        'status': 'success',
        'message': 'Django API is working!',
        'students_count': Student.objects.count(),
        'active_students_count': Student.objects.filter(status='active').count(),
        'graduated_students_count': Student.objects.filter(status='graduated').count(),
        'available_statuses': list(Student.objects.values_list('status', flat=True).distinct()),
    })