# library/views.py

from django.shortcuts import render, get_object_or_404
from django.db import connections
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.core.cache import cache
import json
from functools import reduce
import operator

from .models import Book, Category, Author, Publisher, BookSearch

from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.core.management import call_command
from django.contrib import messages

import csv
from django.http import HttpResponse

def download_csv_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="book_import_template.csv"'

    writer = csv.writer(response)
    header = [
        'title*', 'subtitle', 'author*', 'publisher*', 'publication_year*', 
        'isbn_10', 'isbn_13', 'classification_number*', 'cutter_number*', 
        'category*', 'language', 'pages', 'edition', 'description', 
        'keywords', 'total_copies', 'copies_available', 'location_shelf', 'status'
    ]
    writer.writerow(header)
    writer.writerow([
        'Sample Book Title', 'A Sample Subtitle', 'Author One;Author Two', 'Sample Publisher', '2023',
        '1234567890', '9781234567890', '230.1', 'S64i', 'Systematic Theology', 'en', '450', '3rd Edition',
        'A sample book description.', 'theology,christianity,doctrine', '3', '2', 'A-1-5', 'available'
    ])

    return response


@staff_member_required
def upload_csv(request):
    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            fs = FileSystemStorage(location='media/library/csv_uploads')
            filename = fs.save(csv_file.name, csv_file)
            file_path = fs.path(filename)
            
            try:
                call_command('import_books', file_path)
                messages.success(request, f'Successfully imported books from {filename}.')
            except Exception as e:
                messages.error(request, f'Error importing books: {e}')
            
            return render(request, 'library/upload_csv.html')
        else:
            messages.error(request, 'No CSV file selected.')

    return render(request, 'library/upload_csv.html')



def library_home(request):
    """Display a comprehensive, filterable list of books."""
    books = Book.objects.select_related('publisher', 'category').prefetch_related('authors').all()
    query = request.GET.get('q', '').strip()

    # Enhanced full-text search
    if query:
        using_postgres = connections['default'].vendor == 'postgresql'
        if using_postgres:
            search_vector = (
                SearchVector('title', weight='A') + 
                SearchVector('subtitle', weight='B') +
                SearchVector('authors__first_name', weight='B') +
                SearchVector('authors__last_name', weight='B') + 
                SearchVector('isbn_10', weight='C') +
                SearchVector('isbn_13', weight='C') +
                SearchVector('keywords', weight='C') +
                SearchVector('call_number', weight='D')
            )
            search_query = SearchQuery(query)
            books = books.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.1).order_by('-rank')
            
            # Track search for analytics
            try:
                search_obj, created = BookSearch.objects.get_or_create(query=query)
                if not created:
                    search_obj.search_count += 1
                    search_obj.save()
            except:
                pass  # Don't fail if search tracking fails
        else:
            # Enhanced SQLite search - searches titles, authors, and more
            query_words = query.split()
            final_q = Q()
            
            for word in query_words:
                word_q = (
                    Q(title__icontains=word) |
                    Q(subtitle__icontains=word) |
                    Q(authors__first_name__icontains=word) |
                    Q(authors__last_name__icontains=word) |
                    Q(isbn_10__icontains=word) |
                    Q(isbn_13__icontains=word) |
                    Q(keywords__icontains=word) |
                    Q(call_number__icontains=word) |
                    Q(publisher__name__icontains=word) |
                    Q(category__name__icontains=word)
                )
                final_q &= word_q
            
            if final_q:
                books = books.filter(final_q).distinct()
                
                # Track search for analytics
                try:
                    search_obj, created = BookSearch.objects.get_or_create(query=query)
                    if not created:
                        search_obj.search_count += 1
                        search_obj.save()
                except:
                    pass  # Don't fail if search tracking fails
            else:
                books = books.none()

    # Filters
    category_slug = request.GET.get('category')
    author_slug = request.GET.get('author')
    status = request.GET.get('status')
    
    if category_slug:
        books = books.filter(category__slug=category_slug)
    if author_slug:
        books = books.filter(authors__slug=author_slug)
    if status:
        if status == 'available':
            books = books.filter(status='available', copies_available__gt=0)
        else:
            books = books.filter(status=status)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['title', '-title', '-publication_year', 'publication_year', '-times_borrowed', 'times_borrowed', '-created_at', 'created_at', 'call_number', '-call_number']
    if sort_by in valid_sorts:
        books = books.order_by(sort_by)

    # Pagination
    paginator = Paginator(books, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Filter options for sidebar
    filter_options = cache.get('library_filter_options')
    if not filter_options:
        filter_options = {
            'categories': Category.objects.annotate(book_count=Count('books')).filter(book_count__gt=0).order_by('name'),
            'authors': Author.objects.annotate(book_count=Count('books')).filter(book_count__gt=0).order_by('last_name', 'first_name'),
        }
        cache.set('library_filter_options', filter_options, 60 * 15) # Cache for 15 minutes

    context = {
        'page_obj': page_obj,
        'filter_options': filter_options,
        'selected_filters': {
            'category': category_slug,
            'author': author_slug,
            'status': status,
        },
        'search_query': query,
        'sort_by': sort_by,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'library/partials/book_grid.html', context)

    return render(request, 'library/home.html', context)



def book_detail(request, slug):
    """Display detailed view of a single book"""
    book = get_object_or_404(
        Book.objects.select_related('publisher', 'category').prefetch_related('authors'), 
        slug=slug
    )
    
    # Related books (same category or authors)
    related_books = Book.objects.filter(
        Q(category=book.category) | Q(authors__in=book.authors.all())
    ).exclude(id=book.id).distinct().select_related('publisher', 'category').prefetch_related('authors')[:6]
    
    context = {
        'book': book,
        'related_books': related_books,
    }
    return render(request, 'library/book_detail.html', context)



@require_http_methods(["GET"])
def quick_search(request):
    """HTMX quick search for autocomplete - searches titles and authors"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return render(request, 'library/partials/quick_search_results.html', {'results': [], 'query': query})
    
    using_postgres = connections['default'].vendor == 'postgresql'

    if using_postgres:
        # Full-text search for PostgreSQL
        search_vector = (
            SearchVector('title', weight='A') +
            SearchVector('subtitle', weight='B') +
            SearchVector('authors__first_name', weight='B') +
            SearchVector('authors__last_name', weight='B') +
            SearchVector('call_number', weight='C') +
            SearchVector('isbn_10', weight='C') +
            SearchVector('isbn_13', weight='C')
        )
        search_query = SearchQuery(query)
        books = Book.objects.select_related('publisher', 'category').prefetch_related('authors').annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.1).order_by('-rank')[:8]
    else:
        # Enhanced search for SQLite - searches titles, subtitles, and authors
        query_words = query.split()
        books_queryset = Book.objects.select_related('publisher', 'category').prefetch_related('authors')
        
        # Build search query for each word
        final_q = Q()
        for word in query_words:
            word_q = (
                Q(title__icontains=word) |
                Q(subtitle__icontains=word) |
                Q(authors__first_name__icontains=word) |
                Q(authors__last_name__icontains=word) |
                Q(call_number__icontains=word) |
                Q(isbn_10__icontains=word) |
                Q(isbn_13__icontains=word) |
                Q(keywords__icontains=word)
            )
            final_q &= word_q
        
        if final_q:
            books = books_queryset.filter(final_q).distinct()[:8]
        else:
            books = Book.objects.none()

    return render(request, 'library/partials/quick_search_results.html', {
        'results': books, 
        'query': query
    })

def category_list(request):
    """Display all categories"""
    categories = cache.get('library_category_list')
    if not categories:
        categories = Category.objects.annotate(
            book_count=Count('books')
        ).order_by('name')
        cache.set('library_category_list', categories, 60 * 15) # Cache for 15 minutes
    
    context = {
        'categories': categories,
    }
    return render(request, 'library/category_list.html', context)

def category_books(request, slug):
    """Display books in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category).select_related('publisher', 'category').prefetch_related('authors')
    
    # Pagination
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'library/category_books.html', context)

def author_list(request):
    """Display all authors"""
    authors = cache.get('library_author_list')
    if not authors:
        authors = Author.objects.annotate(
            book_count=Count('books')
        ).order_by('last_name', 'first_name')
        cache.set('library_author_list', authors, 60 * 15) # Cache for 15 minutes
    
    # Pagination
    paginator = Paginator(authors, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'library/author_list.html', context)

def author_detail(request, slug):
    """Display author details and their books"""
    author = get_object_or_404(Author, slug=slug)
    books = Book.objects.filter(authors=author).select_related('publisher', 'category').prefetch_related('authors')
    
    # Pagination
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'library/author_detail.html', context)

def publisher_list(request):
    """Display all publishers"""
    publishers = cache.get('library_publisher_list')
    if not publishers:
        publishers = Publisher.objects.annotate(
            book_count=Count('books')
        ).order_by('name')
        cache.set('library_publisher_list', publishers, 60 * 15) # Cache for 15 minutes
    
    # Pagination
    paginator = Paginator(publishers, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'library/publisher_list.html', context)

def publisher_detail(request, slug):
    """Display publisher details and their books"""
    publisher = get_object_or_404(Publisher, slug=slug)
    books = Book.objects.filter(publisher=publisher).select_related('publisher', 'category').prefetch_related('authors')
    
    # Pagination
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'publisher': publisher,
        'page_obj': page_obj,
    }
    return render(request, 'library/publisher_detail.html', context)

# HTMX Views for dynamic loading
@require_http_methods(["GET"])
def load_more_books(request):
    """Load more books for infinite scroll"""
    page = request.GET.get('page', 1)
    books = Book.objects.select_related('publisher', 'category').prefetch_related('authors').all()
    
    # Apply same filters as book_list view
    category_slug = request.GET.get('category')
    if category_slug:
        books = books.filter(category__slug=category_slug)
    
    paginator = Paginator(books, 12)
    page_obj = paginator.get_page(page)
    
    context = {'page_obj': page_obj}
    return render(request, 'library/partials/book_cards.html', context)

def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return render(request, 'library/partials/search_suggestions.html', {'suggestions': []})

    # Split the query into words
    query_words = query.split()

    # Create a Q object for each word
    q_objects = [Q(title__icontains=word) for word in query_words]

    # Chain the Q objects with AND operator
    if q_objects:
        books = Book.objects.filter(reduce(operator.and_, q_objects)).values_list('title', flat=True).distinct()[:10]
    else:
        books = []
    
    suggestions = list(books)
    
    return render(request, 'library/partials/search_suggestions.html', {'suggestions': suggestions})

def get_authors_for_category(request):
    category_slug = request.GET.get('category')
    authors = Author.objects.all()
    if category_slug:
        authors = authors.filter(books__category__slug=category_slug).distinct()
    
    return render(request, 'library/partials/author_options.html', {'authors': authors.order_by('last_name', 'first_name')})