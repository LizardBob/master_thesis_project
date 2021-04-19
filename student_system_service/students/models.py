from django.db import models
from student_system_service.users.models import User


class Student(User):
    index_code = models.CharField(max_length=255, help_text="Student index code similar to id.")
