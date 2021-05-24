import graphene
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from student_system_service.core.utils import get_paginator
from student_system_service.courses.schema import FacultyType

from ..courses.models import Course
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


class StudentPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(StudentType)


class Query(graphene.ObjectType):
    all_students = graphene.Field(StudentPaginatedType, page=graphene.Int())
    student_by_id = graphene.Field(StudentType, id=graphene.String(required=True))

    def resolve_all_students(root, info, page):
        qs = (
            Student.objects.prefetch_related(
                Prefetch("courses", queryset=Course.objects.just_ids())
            )
            .select_related(
                "faculty",
            )
            .all()
        )  # noqa
        return get_paginator(qs, 100, page, StudentPaginatedType)

    def resolve_student_by_id(root, info, id):
        return get_object_or_404(Student, pk=id)
