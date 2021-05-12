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
