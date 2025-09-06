# library/models.py

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Category(models.Model):
    """Book categories/subjects"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Publisher(models.Model):
    """Publishers"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    established_year = models.PositiveIntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(2025)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    """Authors"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    bio = models.TextField(blank=True)
    birth_year = models.PositiveIntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(2025)
        ]
    )
    death_year = models.PositiveIntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(2025)
        ]
    )
    nationality = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            full_name = f"{self.first_name}-{self.last_name}"
            self.slug = slugify(full_name)
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name

class Book(models.Model):
    """Main Book model"""
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('bn', 'Bangla'),
        ('hi', 'Hindi'),
        ('ur', 'Urdu'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('la', 'Latin'),
        ('gr', 'Greek'),
        ('he', 'Hebrew'),
        ('ar', 'Arabic'),
        ('other', 'Other'),
    ]
    
    AVAILABILITY_STATUS = [
        ('available', 'Available'),
        ('checked_out', 'Checked Out'),
        ('reserved', 'Reserved'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
        ('repair', 'Under Repair'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    publication_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(2025)
        ]
    )
    
    # ISBN and Classification
    isbn_10 = models.CharField(max_length=10, blank=True, help_text="10-digit ISBN")
    isbn_13 = models.CharField(max_length=13, blank=True, help_text="13-digit ISBN")
    classification_number = models.CharField(
        max_length=50, 
        help_text="Dewey Decimal Classification (e.g., 236.5)"
    )
    cutter_number = models.CharField(
        max_length=50, 
        help_text="Cutter number (e.g., L43n)"
    )
    call_number = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Auto-generated from classification + cutter number"
    )
    
    # Content Details
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    pages = models.PositiveIntegerField(blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    keywords = models.CharField(
        max_length=500, 
        blank=True, 
        help_text="Comma-separated keywords for better searchability"
    )
    
    # Physical Details
    total_copies = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)
    location_shelf = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Physical location in library (e.g., A-1-3)"
    )
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='available')
    acquisition_date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Cover image
    cover_image = models.ImageField(upload_to='library/covers/', blank=True, null=True)
    
    # Tracking
    times_borrowed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['call_number']),
            models.Index(fields=['isbn_13']),
            models.Index(fields=['classification_number']),
            models.Index(fields=['-created_at']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            counter = 1
            original_slug = self.slug
            while Book.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Auto-generate call number
        if self.classification_number and self.cutter_number:
            self.call_number = f"{self.classification_number} {self.cutter_number}"
        
        # Ensure copies_available doesn't exceed total_copies
        if self.copies_available > self.total_copies:
            self.copies_available = self.total_copies
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('library:book_detail', kwargs={'slug': self.slug})
    
    @property
    def is_available(self):
        return self.copies_available > 0 and self.status == 'available'
    
    @property
    def authors_list(self):
        return ", ".join([author.full_name for author in self.authors.all()])
    
    @property
    def primary_isbn(self):
        return self.isbn_13 if self.isbn_13 else self.isbn_10
    
    def __str__(self):
        return f"{self.title} - {self.authors_list}"

class BookSearch(models.Model):
    """Track popular searches for analytics"""
    query = models.CharField(max_length=200)
    search_count = models.PositiveIntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-search_count', '-last_searched']
    
    def __str__(self):
        return f"{self.query} ({self.search_count} searches)"