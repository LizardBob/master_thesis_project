import graphene

from student_system_service.courses.schema import Query as FacultyQuery
from student_system_service.students.schema import Query as StudentQuery


class Query(FacultyQuery, StudentQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
