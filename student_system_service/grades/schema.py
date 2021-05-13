import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

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


class Query(graphene.ObjectType):
    all_grades = graphene.List(GradeType)
    grade_by_id = graphene.Field(GradeType, id=graphene.String(required=True))

    def resolve_all_grades(root, info):
        return Grade.objects.all()
        # return Grade.objects.select_related('obtained_by', 'provided_by').all()

    def resolve_grade_by_id(root, info, id):
        return get_object_or_404(Grade, pk=id)
