from rest_framework import serializers

from student_system_service.courses.models import Course, Faculty


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "course_code",
            "course_kind",
            "ects_for_course",
            "faculty",
            "grades",
            "lecturer",
        )
