from django.db import models

from .consts import CourseType

from student_system_service.grades.models import Grade


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return f"Faculty {self.name}"


class Course(models.Model):
    name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=255, null=True)
    course_type = models.CharField(
        max_length=10, choices=CourseType.COURSE_TYPE_CHOICES
    )
    ects_for_course = models.SmallIntegerField(default=1)
    faculty = models.ForeignKey(
        Faculty,
        related_name="courses",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    grades = models.ManyToManyField(Grade, blank=True)

    def __str__(self):
        return f"Course at {self.faculty.name}: {self.name} | {self.course_type}"
