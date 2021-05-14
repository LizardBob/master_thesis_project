from rest_framework import serializers

from student_system_service.students.models import Student


class StudentSerializer(serializers.ModelSerializer):
    # TODO add course Serializer
    class Meta:
        model = Student
        fields = ("id", "password", "username", "email", "name", "faculty", "courses")
