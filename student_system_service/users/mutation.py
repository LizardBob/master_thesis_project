import graphene
from django.shortcuts import get_object_or_404
from graphene_django.rest_framework.mutation import SerializerMutation

from student_system_service.users.api.serializers import LecturerSerializer
from student_system_service.users.models import Lecturer
from student_system_service.users.schema import LecturerType


class LecturerInput(graphene.InputObjectType):
    """
    Example of payload objects properties:
    "password": "123",
        "username": "Lect_Test",
        "email": "lecTest@test.com",
        "name": "K Drapa",
    """

    password = graphene.String()
    username = graphene.String()
    email = graphene.String()
    name = graphene.String()


class LecturerCreateMutation(graphene.Mutation):
    class Arguments:
        input_data = LecturerInput(required=True)

    lecturer = graphene.Field(LecturerType)

    def mutate(self, info, input_data):
        lecturer = Lecturer.objects.create(**input_data)

        return LecturerCreateMutation(lecturer=lecturer)


class LecturerUpdateMutation(SerializerMutation):
    class Meta:
        serializer_class = LecturerSerializer
        model_operations = ["update"]
        lookup_field = "id"


class LecturerDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, *args, **kwargs):
        lecturer = get_object_or_404(Lecturer, pk=kwargs.get("id"))
        lecturer.delete()

        return LecturerDeleteMutation(ok=True)


class Mutation(graphene.ObjectType):
    create_lecturer = LecturerCreateMutation.Field(required=True)
    update_lecturer = LecturerUpdateMutation.Field()
    delete_lecturer = LecturerDeleteMutation.Field()
