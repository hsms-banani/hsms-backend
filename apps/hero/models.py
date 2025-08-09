# models.py
from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from PIL import Image
import os

class HeroSlide(models.Model):
    title = models.CharField(max_length=200, help_text="Main title for the hero slide")
    subtitle = models.TextField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Optional subtitle description"
    )
    image = models.ImageField(
        upload_to='hero_slides/',
        help_text="Upload hero slide image (recommended: 1920x800px)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this slide should be displayed"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"

    def __str__(self):
        return f"{self.title} (Order: {self.order})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Resize image if it's too large
        if self.image:
            img_path = self.image.path
            with Image.open(img_path) as img:
                # Convert RGBA to RGB if necessary
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                # Resize if image is larger than 1920x800
                if img.width > 1920 or img.height > 800:
                    # Maintain aspect ratio
                    img.thumbnail((1920, 800), Image.Resampling.LANCZOS)
                    img.save(img_path, optimize=True, quality=85)

    def delete(self, *args, **kwargs):
        # Delete the image file when the model instance is deleted
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    @property
    def image_url(self):
        """Return the full URL of the image"""
        if self.image:
            return self.image.url
        return None
