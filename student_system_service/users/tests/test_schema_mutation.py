import json

import pytest

from student_system_service.users.models import Lecturer


@pytest.mark.django_db
def test_create_lecturer_mutation(client_query, simple_lecturers):
    operation_name = "createLecturer"
    data = {
        "password": "123",
        "username": "Lect_Test",
        "email": "lecTest@test.com",
        "name": "K Drapa",
    }
    response = client_query(
        """
        mutation createLecturer($input: LecturerInput!) {
          createLecturer(inputData: $input) {
            lecturer {
              id
              indexCode
              name
              email
              username
              courses {
                id
                name
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

    res_json = content.get("data").get(operation_name).get("lecturer")
    assert Lecturer.objects.count() == 4
    new_lecturer = Lecturer.objects.last()

    assert res_json.get("id") == f"{new_lecturer.id}"
    assert res_json.get("courses") == list(new_lecturer.course_set.all())
    assert res_json.get("username") == new_lecturer.username
    assert res_json.get("email") == new_lecturer.email
    assert res_json.get("name") == new_lecturer.name
    assert res_json.get("indexCode") == new_lecturer.index_code


@pytest.mark.django_db
def test_update_lecturer_mutation(client_query, simple_lecturers):
    updating_lecturer = simple_lecturers[-1]
    operation_name = "updateLecturer"
    data = {
        "id": updating_lecturer.id,
        "password": "432",
        "username": "TestL4ec",
        "email": "TestLec@test.com",
        "name": "DrapaK",
    }
    response = client_query(
        """
        mutation updateLecturer($input: LecturerUpdateMutationInput!) {
          updateLecturer(input: $input) {
            id
            password
            email
            username
            name
            courses
          }
        }
        """,
        op_name=operation_name,
        input_data=data,
    )
    content = json.loads(response.content)

    assert "errors" not in content
    updating_lecturer.refresh_from_db()
    res_json = content.get("data").get(operation_name)

    assert updating_lecturer.id == res_json.get("id")
    assert updating_lecturer.password == res_json.get("password")
    assert updating_lecturer.username == res_json.get("username")
    assert updating_lecturer.email == res_json.get("email")
    assert updating_lecturer.name == res_json.get("name")


@pytest.mark.django_db
def test_delete_lecturer_mutation(client_query, simple_lecturers):
    deleting_lecturer = simple_lecturers[-1]
    operation_name = "deleteLecturer"
    response = client_query(
        """
        mutation deleteLecturer($id: Int) {
          deleteLecturer(id: $id) {
            ok
          }
        }
        """,
        op_name=operation_name,
        variables={"id": deleting_lecturer.id},
    )

    content = json.loads(response.content)
    assert "errors" not in content

    res_json = content.get("data").get(operation_name)
    assert res_json.get("ok")
    assert Lecturer.objects.count() == 2
