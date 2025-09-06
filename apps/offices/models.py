# offices/models.py
from django.db import models

class Secretary(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Committee(models.Model):
    COMMITTEE_CHOICES = [
        ('editorial', 'Editorial'),
        ('cultural', 'Cultural'),
        ('pastoral', 'Pastoral'),
        ('liturgical', 'Liturgical'),
    ]
    name = models.CharField(max_length=200, choices=COMMITTEE_CHOICES, unique=True)
    description = models.TextField()
    members = models.TextField(help_text="List of members (comma-separated)")

    def __str__(self):
        return self.get_name_display()