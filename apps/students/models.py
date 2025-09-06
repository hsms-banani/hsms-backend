# students/models.py
from django.db import models
from django.core.validators import FileExtensionValidator

class Student(models.Model):
    name = models.CharField(max_length=200)
    congregation = models.CharField(max_length=200)
    diocese = models.CharField(max_length=200)
    year_joined = models.CharField(max_length=4)
    student_id = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('transferred', 'Transferred'),
        ('suspended', 'Suspended')
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class EnrollmentRequirement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_mandatory = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class ExamInformation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    exam_date = models.DateField()
    exam_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    exam_type = models.CharField(max_length=50, choices=[
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('entrance', 'Entrance'),
        ('comprehensive', 'Comprehensive')
    ], default='final')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-exam_date']

    def __str__(self):
        return f"{self.title} - {self.exam_date}"

class TuitionFee(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    academic_year = models.CharField(max_length=20, blank=True)
    fee_type = models.CharField(max_length=50, choices=[
        ('tuition', 'Tuition'),
        ('registration', 'Registration'),
        ('library', 'Library'),
        ('laboratory', 'Laboratory'),
        ('accommodation', 'Accommodation'),
        ('other', 'Other')
    ], default='tuition')
    is_active = models.BooleanField(default=True)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fee_type', 'title']

    def __str__(self):
        return f"{self.title} - ${self.amount}"

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(
        upload_to='student_documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png'])]
    )
    category = models.CharField(max_length=100, choices=[
        ('forms', 'Forms'),
        ('requirements', 'Requirements'),
        ('guidelines', 'Guidelines'),
        ('handbooks', 'Handbooks'),
        ('applications', 'Applications'),
        ('other', 'Other')
    ], default='forms')
    description = models.TextField(blank=True)
    is_required = models.BooleanField(default=False)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, choices=[
        ('admission', 'Admission'),
        ('academic', 'Academic'),
        ('financial', 'Financial'),
        ('student_life', 'Student Life'),
        ('spiritual', 'Spiritual'),
        ('general', 'General')
    ], default='general')
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'order', 'question']

    def __str__(self):
        return self.question

class SpiritualGuidance(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, choices=[
        ('prayer', 'Prayer'),
        ('meditation', 'Meditation'),
        ('scripture', 'Scripture'),
        ('reflection', 'Reflection'),
        ('guidance', 'Guidance'),
        ('inspiration', 'Inspiration')
    ], default='guidance')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title