from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from student_system_service.grades.api.serializers import GradeSerializer
from student_system_service.grades.models import Grade


class GradeViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    view_tag = ["Grade_tag"]
