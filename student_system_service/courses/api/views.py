from django.db.models import Prefetch
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from student_system_service.courses.api.serializers import (
    CourseSerializer,
    FacultySerializer,
)
from student_system_service.courses.models import Course, Faculty
from student_system_service.grades.models import Grade


class FacultyViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()
    view_tag = ["Faculty_tag"]


class CourseViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    view_tag = ["Course_tag"]

    def get_queryset(self):
        queryset = (
            Course.objects.select_related("lecturer", "faculty")
            .all()
            .prefetch_related(Prefetch("grades", queryset=Grade.objects.only("id")))
        )
        return queryset
