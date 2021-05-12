from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from student_system_service.courses.api.serializers import FacultySerializer
from student_system_service.courses.models import Faculty


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
