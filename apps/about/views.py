# about/views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    AboutSection, AcademicAuthority, MissionVision,
    AcademicCalendar, History, Formation, RulesRegulations,
    FeaturedSection, RectorMessage, AcademicDepartment, 
    FormationStep, CommitteeOffice
)
from .serializers import (
    AboutSectionSerializer, AcademicAuthoritySerializer,
    MissionVisionSerializer, AcademicCalendarSerializer, HistorySerializer,
    FormationSerializer, RulesRegulationsSerializer,
    FeaturedSectionSerializer, RectorMessageSerializer, AcademicDepartmentSerializer,
    FormationStepSerializer, CommitteeOfficeSerializer, FeaturedSectionCompleteSerializer
)

class AboutSectionList(generics.ListAPIView):
    queryset = AboutSection.objects.all()
    serializer_class = AboutSectionSerializer

class AcademicAuthorityList(generics.ListAPIView):
    queryset = AcademicAuthority.objects.all()
    serializer_class = AcademicAuthoritySerializer

class MissionVisionList(generics.ListAPIView):
    queryset = MissionVision.objects.all()
    serializer_class = MissionVisionSerializer

class AcademicCalendarList(generics.ListAPIView):
    queryset = AcademicCalendar.objects.all()
    serializer_class = AcademicCalendarSerializer

class HistoryList(generics.ListAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class FormationList(generics.ListAPIView):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer

class RulesRegulationsList(generics.ListAPIView):
    queryset = RulesRegulations.objects.all()
    serializer_class = RulesRegulationsSerializer

class FeaturedSectionView(generics.ListAPIView):
    serializer_class = FeaturedSectionSerializer
    
    def get_queryset(self):
        return FeaturedSection.objects.filter(is_active=True)

class RectorMessageView(generics.ListAPIView):
    serializer_class = RectorMessageSerializer
    
    def get_queryset(self):
        return RectorMessage.objects.filter(is_active=True).prefetch_related(
            'paragraphs'
        ).order_by('-created_at')

class AcademicDepartmentView(generics.ListAPIView):
    serializer_class = AcademicDepartmentSerializer
    
    def get_queryset(self):
        return AcademicDepartment.objects.filter(is_active=True).prefetch_related('features')

class FormationStepView(generics.ListAPIView):
    serializer_class = FormationStepSerializer
    
    def get_queryset(self):
        return FormationStep.objects.filter(is_active=True)

class CommitteeOfficeView(generics.ListAPIView):
    serializer_class = CommitteeOfficeSerializer
    
    def get_queryset(self):
        return CommitteeOffice.objects.filter(is_active=True)

class FeaturedSectionCompleteView(APIView):
    """
    API endpoint that returns all featured section data in one request
    """
    def get(self, request, format=None):
        try:
            # Get section info
            section_info = FeaturedSection.objects.filter(is_active=True).first()
            
            # Get rector message with paragraphs
            rector_message = RectorMessage.objects.filter(is_active=True).prefetch_related(
                'paragraphs'
            ).first()
            
            # Get departments with features
            departments = AcademicDepartment.objects.filter(is_active=True).prefetch_related('features')
            
            # Get formation steps
            formation_steps = FormationStep.objects.filter(is_active=True)
            
            # Get committees and offices
            committees_offices = CommitteeOffice.objects.filter(is_active=True)
            
            # Serialize the data
            data = {
                'section_info': FeaturedSectionSerializer(section_info, context={'request': request}).data if section_info else None,
                'rector_message': RectorMessageSerializer(rector_message, context={'request': request}).data if rector_message else None,
                'departments': AcademicDepartmentSerializer(departments, many=True, context={'request': request}).data,
                'formation_steps': FormationStepSerializer(formation_steps, many=True).data,
                'committees_offices': CommitteeOfficeSerializer(committees_offices, many=True).data,
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )