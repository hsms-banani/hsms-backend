# academics/models.py
from django.db import models
from django.core.validators import ValidationError
from django.utils import timezone
from datetime import date

class FacultyMember(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)  # Changed from position to match template
    bio = models.TextField(blank=True, null=True)  # Made optional
    email = models.EmailField(blank=True, null=True)  # Added optional email
    image = models.ImageField(upload_to='faculty_images/', blank=True, null=True)  # Added image field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Faculty Member"
        verbose_name_plural = "Faculty Members"

    def __str__(self):
        return f"{self.name} - {self.designation}"

class Professor(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to='professor_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.department}"

class CourseDescription(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ResearchPaper(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    file = models.FileField(upload_to='research_papers/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Thesis(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    file = models.FileField(upload_to='theses/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class AcademicYear(models.Model):
    """Model to represent an academic year"""
    year = models.CharField(max_length=20, unique=True, help_text="e.g., 2024-2025")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False, help_text="Mark as current academic year")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError("End date must be after start date")
        
        if self.is_current:
            # Ensure only one academic year is marked as current
            current_years = AcademicYear.objects.filter(is_current=True)
            if self.pk:
                current_years = current_years.exclude(pk=self.pk)
            if current_years.exists():
                raise ValidationError("Only one academic year can be marked as current")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.year

class EventCategory(models.Model):
    """Categories for calendar events"""
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"

    def __str__(self):
        return self.name

class CalendarEvent(models.Model):
    """Model for academic calendar events"""
    EVENT_TYPES = [
        ('holiday', 'Holiday'),
        ('exam', 'Examination'),
        ('registration', 'Registration'),
        ('semester', 'Semester'),
        ('orientation', 'Orientation'),
        ('graduation', 'Graduation'),
        ('deadline', 'Deadline'),
        ('meeting', 'Meeting'),
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='events')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='events')
    
    # Date and time fields
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_all_day = models.BooleanField(default=True)
    
    # Additional fields
    location = models.CharField(max_length=200, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=50, blank=True, null=True, 
                                        help_text="e.g., weekly, monthly, yearly")
    
    # Status and visibility
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', 'start_time']
        verbose_name = "Calendar Event"
        verbose_name_plural = "Calendar Events"

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after or equal to start date")
        
        if not self.is_all_day and self.start_time and self.end_time:
            if self.start_date == self.end_date and self.start_time >= self.end_time:
                raise ValidationError("End time must be after start time for same-day events")

    def save(self, *args, **kwargs):
        self.clean()
        if not self.end_date:
            self.end_date = self.start_date
        super().save(*args, **kwargs)

    @property
    def is_multi_day(self):
        return self.end_date and self.start_date != self.end_date

    @property
    def duration_days(self):
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1

    @property
    def is_past(self):
        return self.end_date < date.today() if self.end_date else self.start_date < date.today()

    @property
    def is_current(self):
        today = date.today()
        return self.start_date <= today <= (self.end_date or self.start_date)

    @property
    def is_upcoming(self):
        return self.start_date > date.today()

    def __str__(self):
        return f"{self.title} ({self.start_date})"

class CalendarSettings(models.Model):
    """Global settings for the academic calendar"""
    default_academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, 
                                            related_name='default_settings')
    show_weekends = models.BooleanField(default=True)
    default_view = models.CharField(max_length=20, choices=[
        ('month', 'Monthly'),
        ('week', 'Weekly'),
        ('day', 'Daily'),
        ('list', 'List View'),
    ], default='month')
    events_per_page = models.IntegerField(default=10)
    allow_public_view = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Calendar Settings"
        verbose_name_plural = "Calendar Settings"

    def __str__(self):
        return f"Calendar Settings - {self.default_academic_year}"