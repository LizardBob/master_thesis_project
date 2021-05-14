import graphene
from django.shortcuts import get_object_or_404
from graphene_django.rest_framework.mutation import SerializerMutation

from ..courses.models import Faculty
from .api.serializers import StudentSerializer
from .models import Student
from .schema import StudentType


class StudentInput(graphene.InputObjectType):
    """
    "password": "123",
        "username": "G_studentQL",
        "email": "gql@test.com",
        "name": "GTest",
        "faculty": str(simple_faculties[0].id)
    """

    password = graphene.String()
    username = graphene.String()
    email = graphene.String()
    name = graphene.String()
    faculty = graphene.Int()


class StudentCreateMutation(graphene.Mutation):
    class Arguments:
        input_data = StudentInput(required=True)

    student = graphene.Field(StudentType)

    def mutate(self, info, input_data):
        faculty = get_object_or_404(Faculty, pk=input_data.pop("faculty"))
        input_data["faculty"] = faculty
        student = Student.objects.create(**input_data)

        return StudentCreateMutation(student=student)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        form = cls.get_form(root, info, **input)
        from graphene_django.types import ErrorType

        if form.is_valid():
            return cls.perform_mutate(form, info)
        else:
            errors = ErrorType.from_errors(form.errors)

            return cls(errors=errors)


class StudentUpdateMutation(SerializerMutation):
    class Meta:
        serializer_class = StudentSerializer
        model_operations = ["update"]
        lookup_field = "id"


class StudentDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, *args, **kwargs):
        student = Student.objects.get(pk=kwargs.get("id"))
        student.delete()

        return StudentDeleteMutation(ok=True)


class Mutation(graphene.ObjectType):
    create_student = StudentCreateMutation.Field(required=True)
    update_student = StudentUpdateMutation.Field()
    delete_student = StudentDeleteMutation.Field()
