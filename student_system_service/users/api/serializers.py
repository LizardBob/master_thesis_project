from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...courses.api.serializers import CourseSerializer
from ..models import Lecturer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class LecturerSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Lecturer
        fields = "__all__"

    def get_courses(self, obj):
        if obj.course_set.exists():
            return CourseSerializer(obj.course_set, many=True).data
        return []
