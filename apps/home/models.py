# home/models.py
from django.db import models

class HomeContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='home/')

    class Meta:
        app_label = 'home' 

    def __str__(self):
        return self.title