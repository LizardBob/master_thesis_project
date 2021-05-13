import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from student_system_service.courses.schema import FacultyType

from .models import Student


class StudentType(DjangoObjectType):
    faculty = graphene.Field(type=FacultyType)

    def resolve_faculty(self, info):
        return self.faculty

    class Meta:
        model = Student
        fields = (
            "id",
            "password",
            "username",
            "email",
            "name",
            "courses",
            "index_code",
        )
        # interfaces = [graphene.relay.Node] # todo add relay soon


class Query(graphene.ObjectType):
    all_students = graphene.List(StudentType)
    student_by_id = graphene.Field(StudentType, id=graphene.String(required=True))

    def resolve_all_students(root, info):
        return Student.objects.all()

    def resolve_student_by_id(root, info, id):
        return get_object_or_404(Student, pk=id)
