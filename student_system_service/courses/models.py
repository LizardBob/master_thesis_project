from django.db import models

from .consts import CourseType


class Course(models.Model):
    course_type = models.CharField(max_length=10, choices=CourseType.COURSE_TYPE_CHOICES)
    ects_for_course = models.SmallIntegerField(default=1)
