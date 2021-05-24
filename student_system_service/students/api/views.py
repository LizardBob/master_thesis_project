from django.db.models import Prefetch
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from student_system_service.courses.models import Course
from student_system_service.students.api.serializers import StudentSerializer
from student_system_service.students.models import Student


class StudentViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    view_tag = ["Students_tag"]

    def get_queryset(self):
        queryset = (
            Student.objects.select_related("faculty")
            .prefetch_related(
                Prefetch("courses", queryset=Course.objects.all().only("id"))
            )
            .all()
        )
        return queryset
