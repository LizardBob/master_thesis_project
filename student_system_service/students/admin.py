from django.contrib import admin
from .models import Student, Faculty


class StudentModelAdmin(admin.ModelAdmin):
    pass


class FacultyModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Student, StudentModelAdmin)
admin.site.register(Faculty, FacultyModelAdmin)
