import graphene


class GradeSimpleInput(graphene.InputObjectType):
    id = graphene.Int()
