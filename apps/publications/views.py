# publications/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import AnkurPublication, DipttoSakhyoPublication
from .serializers import AnkurPublicationSerializer, DipttoSakhyoPublicationSerializer

class AnkurPublicationList(generics.ListAPIView):
    queryset = AnkurPublication.objects.all()
    serializer_class = AnkurPublicationSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class DipttoSakhyoPublicationList(generics.ListAPIView):
    queryset = DipttoSakhyoPublication.objects.all()
    serializer_class = DipttoSakhyoPublicationSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class AnkurPublicationDetail(generics.RetrieveAPIView):
    queryset = AnkurPublication.objects.all()
    serializer_class = AnkurPublicationSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class DipttoSakhyoPublicationDetail(generics.RetrieveAPIView):
    queryset = DipttoSakhyoPublication.objects.all()
    serializer_class = DipttoSakhyoPublicationSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

@api_view(['POST'])
def download_ankur_publication(request, pk):
    """Track download count for Ankur publications"""
    try:
        publication = get_object_or_404(AnkurPublication, pk=pk)
        publication.download_count = F('download_count') + 1
        publication.save(update_fields=['download_count'])
        
        return Response({
            'message': 'Download count updated',
            'download_url': request.build_absolute_uri(publication.pdf_file.url)
        })
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def download_diptto_sakhyo_publication(request, pk):
    """Track download count for Diptto Sakhyo publications"""
    try:
        publication = get_object_or_404(DipttoSakhyoPublication, pk=pk)
        publication.download_count = F('download_count') + 1
        publication.save(update_fields=['download_count'])
        
        return Response({
            'message': 'Download count updated',
            'download_url': request.build_absolute_uri(publication.pdf_file.url)
        })
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )