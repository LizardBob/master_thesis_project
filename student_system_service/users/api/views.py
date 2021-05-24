from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ...courses.models import Course
from ...grades.models import Grade
from ..models import Lecturer
from .serializers import LecturerSerializer, UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    view_tag = ["Users_tag"]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class LecturerViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.all()
    view_tag = ["Lecturer_tag"]

    def get_queryset(self):
        queryset = Lecturer.objects.prefetch_related(
            Prefetch(
                "course_set",
                queryset=Course.objects.select_related("lecturer", "faculty")
                .all()
                .prefetch_related(
                    Prefetch("grades", queryset=Grade.objects.only("id"))
                ),
            )
        ).all()

        return queryset
