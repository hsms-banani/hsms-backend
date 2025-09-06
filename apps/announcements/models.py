# apps/announcements/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    attachment = models.FileField(upload_to='announcements/attachments/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1, help_text="Higher number = higher priority")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True, help_text="Leave blank for no end date")

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title

    def is_current(self):
        now = timezone.now()
        if self.end_date:
            return self.start_date <= now <= self.end_date
        return self.start_date <= now
    
    @property
    def attachment_url(self):
        if self.attachment:
            return self.attachment.url
        return None
    
    @property
    def attachment_name(self):
        if self.attachment:
            return self.attachment.name.split('/')[-1]
        return None