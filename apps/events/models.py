# events/models.py
from django.db import models

class Event(models.Model):
    SEMINAR = 'seminar'
    PROGRAM = 'program'
    EVENT_TYPE_CHOICES = [
        (SEMINAR, 'Seminar'),
        (PROGRAM, 'Program'),
    ]
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    date = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    is_upcoming = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class PhotoGallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='event_photos/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Photo for {self.event.title}"

class VideoGallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField()
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Video for {self.event.title}"