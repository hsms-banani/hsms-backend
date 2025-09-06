# apps/about/models.py - Updated with content cleaning
from django.db import models
from django_summernote.fields import SummernoteTextField
from .utils import clean_summernote_content, process_content_for_display

class AboutSection(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class AcademicAuthority(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = models.TextField()

    def __str__(self):
        return self.name

class MissionVision(models.Model):
    mission = models.TextField()
    vision = models.TextField()

    def __str__(self):
        return "Mission & Vision"

class AcademicCalendar(models.Model):
    year = models.CharField(max_length=10)
    file = models.FileField(upload_to='academic_calendars/')

    def __str__(self):
        return self.year

class History(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Formation(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class RulesRegulations(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class FeaturedSection(models.Model):
    title = models.CharField(max_length=200, default="Excellence in Theological & Philosophical Education")
    subtitle = models.TextField(default="Discover what makes Holy Spirit Major Seminary a center for spiritual and intellectual formation")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Featured Section"
        verbose_name_plural = "Featured Sections"

    def __str__(self):
        return self.title

class RectorMessage(models.Model):
    name = models.CharField(max_length=100, default="Rev. Fr. Paul Gomes")
    position = models.CharField(max_length=100, default="Rector, Holy Spirit Major Seminary")
    image = models.ImageField(upload_to='rector/', help_text="Upload rector's portrait image")
    quote = models.TextField(help_text="Inspirational quote from the rector", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rector Message"
        verbose_name_plural = "Rector Messages"

    def __str__(self):
        return f"Message from {self.name}"

class RectorMessageParagraph(models.Model):
    rector_message = models.ForeignKey(
        RectorMessage, 
        on_delete=models.CASCADE, 
        related_name='paragraphs'
    )
    content = SummernoteTextField(
        help_text="Rich text content for this paragraph with formatting options"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of this paragraph (0 = first, 1 = second, etc.)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rector Message Paragraph"
        verbose_name_plural = "Rector Message Paragraphs"
        ordering = ['order']

    def save(self, *args, **kwargs):
        """Clean content before saving"""
        if self.content:
            self.content = clean_summernote_content(self.content)
        super().save(*args, **kwargs)

    def get_clean_content(self):
        """Get cleaned content for display"""
        return process_content_for_display(self.content)

    def get_plain_text_preview(self, max_length=150):
        """Get plain text preview for admin or summaries"""
        from .utils import extract_plain_text
        return extract_plain_text(self.content, max_length)

    def __str__(self):
        return f"{self.rector_message.name} - Paragraph {self.order + 1}"

class AcademicDepartment(models.Model):
    DEPARTMENT_CHOICES = [
        ('philosophy', 'Philosophy'),
        ('theology', 'Theology'),
    ]
    
    name = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='departments/', help_text="Department image")
    description = models.TextField(help_text="Department description")
    link_url = models.CharField(max_length=200, help_text="Link to department page")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Academic Department"
        verbose_name_plural = "Academic Departments"
        ordering = ['order', 'name']

    def __str__(self):
        return self.display_name

class DepartmentFeature(models.Model):
    department = models.ForeignKey(AcademicDepartment, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Department Feature"
        verbose_name_plural = "Department Features"
        ordering = ['order']

    def __str__(self):
        return f"{self.department.display_name} - {self.title}"

class FormationStep(models.Model):
    step_number = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Formation Step"
        verbose_name_plural = "Formation Steps"
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"

class CommitteeOffice(models.Model):
    ICON_CHOICES = [
        ('book', 'Book (Academic Affairs)'),
        ('heart', 'Heart (Spiritual Formation)'),
        ('users', 'Users (Student Affairs)'),
        ('home', 'Home (Pastoral Ministries)'),
        ('library', 'Library (Library & Research)'),
        ('calculator', 'Calculator (Administration)'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=20, choices=ICON_CHOICES)
    link_url = models.CharField(max_length=200, help_text="Link to committee/office page")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Committee/Office"
        verbose_name_plural = "Committees/Offices"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title