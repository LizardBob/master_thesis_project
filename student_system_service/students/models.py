from django.db import models
from student_system_service.users.models import User
from student_system_service.courses.models import Course


class Student(User):
    index_code = models.CharField(max_length=255, help_text="Student index code similar to id.")
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
