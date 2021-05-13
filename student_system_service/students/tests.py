import json

import pytest

from ..conftest import *  # noqa
from .models import Student


@pytest.mark.django_db
def test_student_model_create(simple_students, simple_faculty):
    for index, simple_student in enumerate(simple_students):
        assert simple_student.username == f"TestStudent_{index}"
        assert simple_student.email == f"student{index}.test@test.com"
        assert simple_student.faculty == simple_faculty
        assert simple_student.index_code == f"s{index + 1}"


@pytest.mark.django_db
def test_all_students_query(client_query, simple_students):
    operation_name = "allStudents"
    response = client_query(
        """
        query allStudents{
          allStudents {
            id
            name
            username
            email
            indexCode
            faculty {
              id
              name
            }
            courses {
              id
              name
              courseCode
              courseType
              ectsForCourse
              faculty {
                id
                name
              }
              grades {
                value
                isFinalGrade
                obtainedBy {
                  id
                  name
                }
              }
            }
          }
        }
        """,
        op_name=operation_name,
    )

    content = json.loads(response.content)
    assert "errors" not in content

    res_json = content.get("data").get(operation_name)
    all_students = Student.objects.all()

    for student in res_json:
        excpected_student = all_students.get(id=student.get("id"))
        assert student.get("username") == excpected_student.username
        assert student.get("email") == excpected_student.email
        assert student.get("name") == excpected_student.name
        assert student.get("faculty").get("id") == str(excpected_student.faculty.id)
        assert student.get("courses") == list(excpected_student.courses.all())


@pytest.mark.django_db
def test_get_student_by_id_query(client_query, simple_students):
    student = simple_students[-1]
    operation_name = "studentById"
    response = client_query(
        """
        query studentById($id: String!) {
          studentById(id: $id) {
            id
            name
            username
            email
            indexCode
            faculty {
              id
              name
            }
            courses {
              id
              name
            }
          }
        }
        """,
        op_name=operation_name,
        variables={"id": student.id},
    )
    content = json.loads(response.content)
    assert "errors" not in content

    result = content.get("data").get(operation_name)

    assert result.get("username") == student.username
    assert result.get("email") == student.email
    assert result.get("name") == student.name
    assert result.get("faculty").get("id") == str(student.faculty.id)
    assert result.get("courses") == list(student.courses.all())
    assert result.get("indexCode") == student.index_code
