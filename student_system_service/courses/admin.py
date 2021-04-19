from django.contrib import admin
from .models import Course


class CourseModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseModelAdmin)
