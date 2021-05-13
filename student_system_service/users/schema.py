import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from .models import Lecturer


class LecturerType(DjangoObjectType):
    class Meta:
        model = Lecturer
        fields = (
            "id",
            "name",
            "username",
            "email",
            "index_code",
        )


class Query(graphene.ObjectType):
    all_lecturers = graphene.List(LecturerType)
    lecturer_by_id = graphene.Field(LecturerType, id=graphene.String(required=True))

    def resolve_all_lecturers(root, info):
        return Lecturer.objects.all()

    def resolve_lecturer_by_id(root, info, id):
        return get_object_or_404(Lecturer, pk=id)
