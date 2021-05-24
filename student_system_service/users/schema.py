import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from ..core.utils import get_paginator
from .models import Lecturer


class LecturerType(DjangoObjectType):
    courses = graphene.Field(graphene.List(graphene.Int))

    def resolve_courses(self, info):
        return self.course_set.just_ids().values_list("id", flat=True)

    class Meta:
        model = Lecturer
        fields = (
            "id",
            "name",
            "username",
            "email",
            "index_code",
            "courses",
        )


class LecturerPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(LecturerType)


class Query(graphene.ObjectType):
    all_lecturers = graphene.Field(LecturerPaginatedType, page=graphene.Int())
    lecturer_by_id = graphene.Field(LecturerType, id=graphene.String(required=True))

    def resolve_all_lecturers(root, info, page):
        return get_paginator(Lecturer.objects.all(), 100, page, LecturerPaginatedType)

    def resolve_lecturer_by_id(root, info, id):
        return get_object_or_404(Lecturer, pk=id)
