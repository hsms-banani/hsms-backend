# apps/news/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import News, NewsCategory
from .serializers import NewsSerializer, NewsCategorySerializer

class NewsListView(ListView):
    model = News
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = News.objects.filter(status='published').select_related('category', 'author')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        return queryset.order_by('-published_at', '-created_at')

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        return News.objects.filter(status='published').select_related('category', 'author')
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.increment_views()
        return obj

class NewsCategoryView(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news_list'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(NewsCategory, slug=self.kwargs['category_slug'])
        return News.objects.filter(
            category=self.category, 
            status='published'
        ).select_related('category', 'author').order_by('-published_at', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# API Views for Frontend
class NewsListPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50

class NewsListAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer
    pagination_class = NewsListPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'featured']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'published_at', 'views_count']
    ordering = ['-published_at', '-created_at']
    
    def get_queryset(self):
        return News.objects.filter(status='published').select_related('category', 'author')

class NewsDetailAPIView(generics.RetrieveAPIView):
    serializer_class = NewsSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return News.objects.filter(status='published').select_related('category', 'author')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

class NewsCategoryAPIView(generics.ListAPIView):
    serializer_class = NewsCategorySerializer
    
    def get_queryset(self):
        return NewsCategory.objects.all().order_by('name')

# Additional API endpoint for latest news (used by homepage)
@api_view(['GET'])
def latest_news(request):
    """Get latest news for homepage"""
    try:
        limit = int(request.GET.get('limit', 3))
        news = News.objects.filter(
            status='published'
        ).select_related(
            'category', 'author'
        ).order_by(
            '-published_at', '-created_at'
        )[:limit]
        
        serializer = NewsSerializer(news, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError:
        return Response(
            {'error': 'Invalid limit parameter'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )