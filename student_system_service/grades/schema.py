import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from ..core.utils import get_paginator
from .models import Grade


class GradeType(DjangoObjectType):
    class Meta:
        model = Grade
        fields = (
            "id",
            "value",
            "is_final_grade",
            "obtained_by",
            "provided_by",
        )


class GradePaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(GradeType)


class Query(graphene.ObjectType):
    all_grades = graphene.Field(GradePaginatedType, page=graphene.Int())
    grade_by_id = graphene.Field(GradeType, id=graphene.String(required=True))

    def resolve_all_grades(root, info, page):
        qs = Grade.objects.select_related("obtained_by", "provided_by").all()
        return get_paginator(qs, 100, page, GradePaginatedType)

    def resolve_grade_by_id(root, info, id):
        return get_object_or_404(Grade, pk=id)
