import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from .models import Course, Faculty


class FacultyType(DjangoObjectType):
    class Meta:
        model = Faculty
        fields = ("id", "name", "students")


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "course_code",
            "course_type",
            "ects_for_course",
            "faculty",
            "grades",
            "lecturer",
        )


class Query(graphene.ObjectType):
    all_faculties = graphene.List(FacultyType)
    faculty_by_id = graphene.Field(FacultyType, id=graphene.String(required=True))

    all_courses = graphene.List(CourseType)
    course_by_id = graphene.Field(CourseType, id=graphene.String(required=True))

    def resolve_all_courses(root, info):
        return Course.objects.all()  # TODO little improvements

    def resolve_course_by_id(root, info, id):
        return get_object_or_404(Course, pk=id)

    def resolve_all_faculties(root, info):
        return Faculty.objects.all()

    def resolve_faculty_by_id(root, info, id):
        return get_object_or_404(Faculty, pk=id)
