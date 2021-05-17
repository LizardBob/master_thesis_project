import graphene
from django.shortcuts import get_object_or_404
from graphene_django.rest_framework.mutation import SerializerMutation

from student_system_service.courses.api.serializers import FacultySerializer
from student_system_service.courses.models import Course, Faculty
from student_system_service.courses.schema import CourseNode, FacultyType
from student_system_service.users.models import Lecturer


class FacultyInput(graphene.InputObjectType):
    """
    Example of payload objects properties :
    "name": "Advanced Programming"
    """

    name = graphene.String(required=True)


class CourseInput(graphene.InputObjectType):
    """
    Exmaple of payload object properties:
    "name": "New Course Programming",
        "course_kind": "laboratory",
        "ects_for_course": 2,
        "faculty": faculty.id,
        "lecturer": lecturer.id,
        "grades": [],
    """

    id = graphene.Int()
    name = graphene.String()
    course_kind = graphene.String()
    ects_for_course = graphene.Int()
    faculty = graphene.Int()
    lecturer = graphene.Int()
    grades = graphene.List(graphene.Int)


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


class CourseCreateMutation(graphene.Mutation):
    class Arguments:
        input_data = CourseInput(required=True)

    course = graphene.Field(CourseNode)

    def mutate(self, info, input_data):
        input_data["faculty"] = get_object_or_404(Faculty, pk=input_data.pop("faculty"))
        input_data["lecturer"] = get_object_or_404(
            Lecturer, pk=input_data.pop("lecturer")
        )
        grades = input_data.pop("grades")
        course = Course.objects.create(**input_data)
        course.grades.set(grades)
        return CourseCreateMutation(course=course)


class CourseUpdateMutation(graphene.Mutation):
    class Arguments:
        input_data = CourseInput(required=True)

    course = graphene.Field(CourseNode)

    def mutate(self, info, input_data):
        # TODO add hanlding grades updates
        grades = input_data.pop("grades")
        Course.objects.filter(id=input_data.get("id")).update(**input_data)
        course = get_object_or_404(Course, pk=input_data.get("id"))
        course.grades.set(grades)

        return CourseCreateMutation(course=course)


class CourseDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get("id"))
        course.delete()

        return CourseDeleteMutation(ok=True)


class Mutation(graphene.ObjectType):
    create_faculty = FacultyCreateMutation.Field()
    update_faculty = FacultyUpdateMutation.Field()
    delete_faculty = FacultyDeleteMutation.Field()

    create_course = CourseCreateMutation.Field()
    update_course = CourseUpdateMutation.Field()
    delete_course = CourseDeleteMutation.Field()
