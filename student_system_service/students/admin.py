from django.contrib import admin
from .models import Student

class StudentModelAdmin(admin.ModelAdmin):
    pass

admin.register(Student, StudentModelAdmin)
