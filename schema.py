import graphene

from student_system_service.courses.mutation import Mutation as FacultyAndCourseMutation
from student_system_service.courses.schema import Query as FacultyAndCourseQuery
from student_system_service.grades.mutation import Mutation as GradeMutation
from student_system_service.grades.schema import Query as GradeQuery
from student_system_service.students.mutation import Mutation as StudentMutation
from student_system_service.students.schema import Query as StudentQuery
from student_system_service.users.mutation import Mutation as LecturerMutation
from student_system_service.users.schema import Query as LecturerQuery


class Query(
    GradeQuery, LecturerQuery, FacultyAndCourseQuery, StudentQuery, graphene.ObjectType
):
    pass


class Mutations(
    GradeMutation,
    FacultyAndCourseMutation,
    LecturerMutation,
    StudentMutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
