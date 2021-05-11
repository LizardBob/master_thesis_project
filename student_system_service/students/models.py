from typing import Iterable, Optional

from django.db import models, transaction
from django.db.models import QuerySet

from student_system_service.courses.models import Course, Faculty
from student_system_service.users.models import User

# class StudentCourse(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.)
#


class Student(User):
    PATTERN_CODE = "s"

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

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        with transaction.atomic():
            student_objects: QuerySet[Student] = self.__class__.objects.order_by("id")
            last_id = (
                student_objects.last().index_code.split(self.PATTERN_CODE)[-1]
                if student_objects.exists()
                else 0
            )
            self.index_code = f"{self.PATTERN_CODE}{int(last_id) + 1}"
            super().save(force_insert, force_update, using, update_fields)

    def student_courses(self) -> QuerySet[Course]:
        return self.courses.all()
