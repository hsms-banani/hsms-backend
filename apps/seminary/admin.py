# seminary/admin.py
from django.contrib import admin
from .models import (
    ChurchHistory, BangladeshHistory, LocalChurchHistory,
    SeminaryHistory, Department, FormationProgram
)

admin.site.register(ChurchHistory)
admin.site.register(BangladeshHistory)
admin.site.register(LocalChurchHistory)
admin.site.register(SeminaryHistory)
admin.site.register(Department)
admin.site.register(FormationProgram)