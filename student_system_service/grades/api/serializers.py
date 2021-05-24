from rest_framework import serializers

from student_system_service.grades.models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ("id", "value", "is_final_grade", "obtained_by", "provided_by")
