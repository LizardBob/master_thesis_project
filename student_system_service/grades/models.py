from django.db import models
from model_utils.models import TimeStampedModel

from .const import GradeValue


class Grade(TimeStampedModel):
    value = models.CharField(max_length=5, choices=GradeValue.GRADE_VALUES_CHOICES)
    is_final_grade = models.BooleanField()
    obtained_by = models.ForeignKey("students.Student", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Grade: {self.value}"
