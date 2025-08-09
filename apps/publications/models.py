# publications/models.py
from django.db import models
from django.core.validators import FileExtensionValidator
import os

class AnkurPublication(models.Model):
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(
        upload_to='publications/ankur/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Upload PDF file only"
    )
    thumbnail = models.ImageField(
        upload_to='publications/ankur/thumbnails/',
        blank=True,
        null=True,
        help_text="Optional thumbnail image for the publication"
    )
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0)
    file_size = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['-date_published']
        verbose_name = "Ankur Publication"
        verbose_name_plural = "Ankur Publications"

    def __str__(self):
        return self.title
    
    def get_file_size(self):
        if self.pdf_file and hasattr(self.pdf_file, 'size'):
            size = self.pdf_file.size
            if size < 1024*1024:
                return f"{size/1024:.1f} KB"
            else:
                return f"{size/(1024*1024):.1f} MB"
        return "Unknown"
    
    def save(self, *args, **kwargs):
        if self.pdf_file:
            self.file_size = self.get_file_size()
        super().save(*args, **kwargs)

class DipttoSakhyoPublication(models.Model):
    title = models.CharField(max_length=200)
    issue = models.CharField(max_length=50)
    pdf_file = models.FileField(
        upload_to='publications/diptto_sakhyo/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Upload PDF file only"
    )
    thumbnail = models.ImageField(
        upload_to='publications/diptto_sakhyo/thumbnails/',
        blank=True,
        null=True,
        help_text="Optional thumbnail image for the publication"
    )
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0)
    file_size = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['-date_published']
        verbose_name = "Diptto Sakhyo Publication"
        verbose_name_plural = "Diptto Sakhyo Publications"

    def __str__(self):
        return f"{self.title} - Issue {self.issue}"
    
    def get_file_size(self):
        if self.pdf_file and hasattr(self.pdf_file, 'size'):
            size = self.pdf_file.size
            if size < 1024*1024:
                return f"{size/1024:.1f} KB"
            else:
                return f"{size/(1024*1024):.1f} MB"
        return "Unknown"
    
    def save(self, *args, **kwargs):
        if self.pdf_file:
            self.file_size = self.get_file_size()
        super().save(*args, **kwargs)