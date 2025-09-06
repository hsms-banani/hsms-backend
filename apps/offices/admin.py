# offices/admin.py
from django.contrib import admin
from .models import Secretary, Committee

admin.site.register(Secretary)
admin.site.register(Committee)