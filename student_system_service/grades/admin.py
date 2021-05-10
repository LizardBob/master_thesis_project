from django.contrib import admin
from .models import Grade


class GradeModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Grade, GradeModelAdmin)
