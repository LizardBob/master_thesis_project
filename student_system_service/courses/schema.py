import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from student_system_service.courses.models import Faculty


class FacultyType(DjangoObjectType):
    class Meta:
        model = Faculty
        fields = ("id", "name", "students")


class Query(graphene.ObjectType):
    all_faculties = graphene.List(FacultyType)
    faculty_by_id = graphene.Field(FacultyType, id=graphene.String(required=True))

    def resolve_all_faculties(root, info):
        return Faculty.objects.all()

    def resolve_faculty_by_id(root, info, id):
        return get_object_or_404(Faculty, pk=id)
