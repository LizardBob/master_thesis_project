from typing import Iterable, Optional

from django.db import models, transaction
from django.db.models import QuerySet

from student_system_service.grades.models import Grade

from .consts import CourseTypes


class CourseQuerySet(models.QuerySet):
    def for_method_get_viewset(self):
        return self.select_related(
            "faculty",
            "lecturer",
        )

    def just_ids(self):
        return self.only("id")


class CourseManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return CourseQuerySet(self.model, using=self._db)

    def for_method_get_viewset(self):
        return self.get_queryset().for_method_get_viewset()

    def just_ids(self):
        return self.get_queryset().just_ids()


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return f"Faculty {self.name}"


class Course(models.Model):
    PATTERN_CODE = "c"

    name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=255, blank=True, null=True)
    course_kind = models.CharField(
        max_length=10, choices=CourseTypes.COURSE_TYPE_CHOICES
    )
    ects_for_course = models.SmallIntegerField(default=1)
    faculty = models.ForeignKey(
        Faculty,
        related_name="courses",
        on_delete=models.DO_NOTHING,
    )
    grades = models.ManyToManyField(Grade, blank=True)
    lecturer = models.ForeignKey("users.Lecturer", on_delete=models.DO_NOTHING)

    objects = CourseManager()

    def __str__(self):
        return f"Course at {self.faculty.name}: {self.name} | {self.course_kind}"

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        with transaction.atomic():
            courses_objects: QuerySet[Course] = self.__class__.objects.order_by("id")
            last_id = (
                courses_objects.last().course_code.split(self.PATTERN_CODE)[-1]
                if courses_objects.exists()
                else 0
            )
            self.course_code = f"{self.PATTERN_CODE}{int(last_id) + 1}"
            super().save(force_insert, force_update, using, update_fields)
