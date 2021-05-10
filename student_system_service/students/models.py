from django.db import models
from student_system_service.users.models import User
from student_system_service.courses.models import Course, Faculty


# class StudentCourse(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.)
#


class Student(User):
    index_code = models.CharField(
        max_length=255,
        help_text="Student index code similar to id.",
        blank=True,
        null=False,
    )
    courses = models.ManyToManyField(Course)
    faculty = models.ForeignKey(
        Faculty,
        related_name="students",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
