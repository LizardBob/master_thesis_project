import graphene
from django.shortcuts import get_object_or_404

from student_system_service.grades.models import Grade
from student_system_service.grades.schema import GradeType
from student_system_service.students.models import Student
from student_system_service.users.models import Lecturer


class GradeInput(graphene.InputObjectType):
    """
    Example of properties in payload object:
    "value": "D",
        "is_final_grade": False,
        "obtained_by": simple_student.id,
        "provided_by": simple_lecturer.id,
    """

    id = graphene.Int()
    value = graphene.String()
    is_final_grade = graphene.Boolean()
    obtained_by = graphene.Int()
    provided_by = graphene.Int()


class GradeCreateMutation(graphene.Mutation):
    class Arguments:
        input_data = GradeInput(required=True)

    grade = graphene.Field(GradeType)

    def mutate(self, info, input_data):
        input_data["obtained_by"] = get_object_or_404(
            Student, pk=input_data.pop("obtained_by")
        )
        input_data["provided_by"] = get_object_or_404(
            Lecturer, pk=input_data.pop("provided_by")
        )
        grade = Grade.objects.create(**input_data)

        return GradeCreateMutation(grade=grade)


class GradeUpdateMutation(graphene.Mutation):
    class Arguments:
        input_data = GradeInput()

    grade = graphene.Field(GradeType)

    def mutate(self, info, input_data):
        input_data["obtained_by"] = get_object_or_404(
            Student, pk=input_data.pop("obtained_by")
        )
        input_data["provided_by"] = get_object_or_404(
            Lecturer, pk=input_data.pop("provided_by")
        )
        Grade.objects.filter(id=input_data.get("id")).update(**input_data)
        grade = get_object_or_404(Grade, pk=input_data.get("id"))

        return GradeUpdateMutation(grade=grade)


class GradeDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, *args, **kwargs):
        grade = get_object_or_404(Grade, pk=kwargs.get("id"))
        grade.delete()

        return GradeDeleteMutation(ok=True)


class Mutation(graphene.ObjectType):
    create_grade = GradeCreateMutation.Field()
    update_grade = GradeUpdateMutation.Field()
    delete_grade = GradeDeleteMutation.Field()
