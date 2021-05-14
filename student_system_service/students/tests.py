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


@pytest.mark.django_db
def test_create_student_mutation(client_query, simple_students, simple_faculties):
    assert simple_students
    operation_name = "createStudent"
    data = {
        "password": "123",
        "username": "G_studentQL",
        "email": "gql@test.com",
        "name": "GTest",
        "faculty": simple_faculties[0].id,
    }
    response = client_query(
        """
        mutation createStudent($input: StudentInput!) {
          createStudent(inputData: $input) {
             student{
                id
                username
                email
                name
                faculty {
                    id
                }
            }
        }
        }
        """,
        op_name=operation_name,
        input_data=data,
    )

    content = json.loads(response.content)
    assert "errors" not in content

    res_json = content.get("data").get(operation_name).get("student")

    assert Student.objects.count() == 4
    new_student = Student.objects.last()

    assert res_json.get("id") == f"{new_student.id}"
    assert new_student.username == res_json.get("username")
    assert new_student.email == res_json.get("email")
    assert new_student.name == res_json.get("name")
    assert f"{new_student.faculty.id}" == res_json.get("faculty").get("id")


@pytest.mark.django_db
def test_update_student_mutation(client_query, simple_students, simple_faculties):
    updating_student = simple_students[-1]
    operation_name = "updateStudent"
    data = {
        "id": updating_student.id,
        "password": "321",
        "username": "H_studentQL",
        "email": "g1q2l@test.com",
        "name": "GTe24st",
        "faculty": simple_faculties[0].id,
    }
    assert updating_student.password != data.get("password")
    assert updating_student.username != data.get("username")
    assert updating_student.email != data.get("email")
    assert updating_student.name != data.get("name")
    assert f"{updating_student.faculty_id}" != data.get("faculty")

    response = client_query(
        """
        mutation updateStudent ($input: StudentUpdateMutationInput!) {
          updateStudent (input: $input) {
            id
            username
            email
            faculty
            name
          }
        }
        """,
        op_name=operation_name,
        input_data=data,
    )

    content = json.loads(response.content)
    import ipdb

    ipdb.set_trace()
    assert "errors" not in content
    updating_student.refresh_from_db()
    res_json = content.get("data").get(operation_name)

    assert updating_student.username == res_json.get("username")
    assert updating_student.email == res_json.get("email")
    assert updating_student.name == res_json.get("name")
    assert f"{updating_student.faculty_id}" == res_json.get("faculty")


@pytest.mark.django_db
def test_delete_student_mutation(client_query, simple_students):
    deleting_student = simple_students[-1]
    operation_name = "deleteStudent"
    response = client_query(
        """
        mutation deleteStudent ($id: Int) {
          deleteStudent(id: $id) {
            ok
          }
        }
        """,
        op_name=operation_name,
        variables={"id": deleting_student.id},
    )
    content = json.loads(response.content)
    assert "errors" not in content

    res_json = content.get("data").get(operation_name)
    assert res_json.get("ok")
    assert Student.objects.count() == 2
