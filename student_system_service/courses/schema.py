import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from ..core.utils import get_paginator
from .models import Course, Faculty


class FacultyType(DjangoObjectType):
    class Meta:
        model = Faculty
        fields = ("id", "name", "students")


class FacultyPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(FacultyType)


class CourseNode(DjangoObjectType):
    grades = graphene.List(graphene.Int)

    def resolve_grades(self, info):
        return self.grades.values_list("id", flat=True)

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


class CoursePaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(CourseNode)


class Query(graphene.ObjectType):
    all_faculties = graphene.Field(FacultyPaginatedType, page=graphene.Int())
    faculty_by_id = graphene.Field(FacultyType, id=graphene.String(required=True))

    all_courses = graphene.Field(CoursePaginatedType, page=graphene.Int())
    course_by_id = graphene.Field(CourseNode, id=graphene.String(required=True))

    def resolve_all_courses(root, info, page):
        return get_paginator(
            Course.objects.for_method_get_viewset(), 100, page, CoursePaginatedType
        )

    def resolve_course_by_id(root, info, id):
        return get_object_or_404(Course, pk=id)

    def resolve_all_faculties(root, info, page):
        # return Faculty.objects.prefetch_related('students').all()
        return get_paginator(Faculty.objects.all(), 100, page, FacultyPaginatedType)

    def resolve_faculty_by_id(root, info, id):
        return get_object_or_404(Faculty, pk=id)
