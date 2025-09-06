from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import HeroSlide
from .serializers import HeroSlideSerializer, HeroSlideListSerializer

class HeroSlideListView(generics.ListAPIView):
    """
    API endpoint to get all active hero slides for the frontend
    """
    serializer_class = HeroSlideListSerializer
    
    def get_queryset(self):
        return HeroSlide.objects.filter(is_active=True).order_by('order', '-created_at')

class HeroSlideDetailView(generics.RetrieveAPIView):
    """
    API endpoint to get a specific hero slide
    """
    queryset = HeroSlide.objects.all()
    serializer_class = HeroSlideSerializer
    lookup_field = 'id'

# CRUD operations for admin or authenticated users
class HeroSlideCreateView(generics.CreateAPIView):
    """
    API endpoint to create a new hero slide
    """
    queryset = HeroSlide.objects.all()
    serializer_class = HeroSlideSerializer

class HeroSlideUpdateView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to update a hero slide
    """
    queryset = HeroSlide.objects.all()
    serializer_class = HeroSlideSerializer
    lookup_field = 'id'

class HeroSlideDeleteView(generics.DestroyAPIView):
    """
    API endpoint to delete a hero slide
    """
    queryset = HeroSlide.objects.all()
    lookup_field = 'id'

# Function-based view for getting active slides (alternative approach)
@api_view(['GET'])
def get_active_hero_slides(request):
    """
    Get all active hero slides in order
    """
    slides = HeroSlide.objects.filter(is_active=True).order_by('order', '-created_at')
    serializer = HeroSlideListSerializer(slides, many=True, context={'request': request})
    return Response({
        'status': 'success',
        'count': len(serializer.data),
        'data': serializer.data
    })

@api_view(['GET'])
def get_hero_slide_by_id(request, slide_id):
    """
    Get a specific hero slide by ID
    """
    try:
        slide = HeroSlide.objects.get(id=slide_id)
        serializer = HeroSlideSerializer(slide, context={'request': request})
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    except HeroSlide.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Hero slide not found'
        }, status=status.HTTP_404_NOT_FOUND)