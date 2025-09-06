from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from library.models import Book, Author, Category, Publisher
from django.db.models import Count, Sum


import json
from django.db.models.functions import TruncMonth

@staff_member_required
def dashboard_home(request):
    """
    View for the custom admin dashboard.
    """
    # Stats overview
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_categories = Category.objects.count()
    total_publishers = Publisher.objects.count()
    total_borrowed = Book.objects.aggregate(total_borrowed=Sum('times_borrowed'))['total_borrowed'] or 0

    # Recent activities
    recent_books = Book.objects.order_by('-created_at')[:5]

    # Top 5 most borrowed books
    most_borrowed_books = Book.objects.order_by('-times_borrowed')[:5]

    # Top 5 authors with most books
    authors_with_most_books = Author.objects.annotate(book_count=Count('books')).order_by('-book_count')[:5]

    # Data for charts
    books_per_category = Category.objects.annotate(book_count=Count('books')).order_by('-book_count')
    category_chart_labels = json.dumps([category.name for category in books_per_category])
    category_chart_data = json.dumps([category.book_count for category in books_per_category])

    books_added_over_time = Book.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    timeline_chart_labels = json.dumps([entry['month'].strftime('%b %Y') for entry in books_added_over_time])
    timeline_chart_data = json.dumps([entry['count'] for entry in books_added_over_time])


    context = {
        'total_books': total_books,
        'total_authors': total_authors,
        'total_categories': total_categories,
        'total_publishers': total_publishers,
        'total_borrowed': total_borrowed,
        'recent_books': recent_books,
        'most_borrowed_books': most_borrowed_books,
        'authors_with_most_books': authors_with_most_books,
        'title': 'Library Dashboard',
        'category_chart_labels': category_chart_labels,
        'category_chart_data': category_chart_data,
        'timeline_chart_labels': timeline_chart_labels,
        'timeline_chart_data': timeline_chart_data,
    }
    return render(request, 'dashboard/home.html', context)