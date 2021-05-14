import graphene
from django.shortcuts import get_object_or_404
from graphene_django.rest_framework.mutation import SerializerMutation

from student_system_service.courses.api.serializers import FacultySerializer
from student_system_service.courses.models import Faculty
from student_system_service.courses.schema import FacultyType


class FacultyInput(graphene.InputObjectType):
    """
    Example of payload objects properties :
    "name": "Advanced Programming"
    """

    name = graphene.String(required=True)


class FacultyCreateMutation(graphene.Mutation):
    class Arguments:
        input_data = FacultyInput(required=True)

    faculty = graphene.Field(FacultyType)

    def mutate(self, info, input_data):
        faculty = Faculty.objects.create(**input_data)

        return FacultyCreateMutation(faculty=faculty)


class FacultyUpdateMutation(SerializerMutation):
    class Meta:
        serializer_class = FacultySerializer
        model_operations = ["update"]
        lookup_field = "id"


class FacultyDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, *args, **kwargs):
        faculty = get_object_or_404(Faculty, pk=kwargs.get("id"))
        faculty.delete()

        return FacultyDeleteMutation(ok=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        form = cls.get_form(root, info, **input)
        from graphene_django.types import ErrorType

        if form.is_valid():
            return cls.perform_mutate(form, info)
        else:
            errors = ErrorType.from_errors(form.errors)

            return cls(errors=errors)


class Mutation(graphene.ObjectType):
    create_faculty = FacultyCreateMutation.Field()
    update_faculty = FacultyUpdateMutation.Field()
    delete_faculty = FacultyDeleteMutation.Field()
