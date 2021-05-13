import graphene

from student_system_service.courses.schema import Query as FacultyAndCourseQuery
from student_system_service.grades.schema import Query as GradeQuery
from student_system_service.students.schema import Query as StudentQuery
from student_system_service.users.schema import Query as LecturerQuery


class Query(
    GradeQuery, LecturerQuery, FacultyAndCourseQuery, StudentQuery, graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
