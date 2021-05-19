import json

import pytest

from student_system_service.conftest import *  # noqa

from ..models import Lecturer


@pytest.mark.django_db
def test_get_all_lecturers_query(client_query, simple_lecturers):
    operation_name = "allLecturers"
    response = client_query(
        """
        query allLecturers {
          allLecturers (page: 1) {
            page
            pages
            hasNext
            hasPrev
            objects{
              id
            indexCode
            email
            username
            name
            courses {
              id
              name
              courseCode
              courseKind
              ectsForCourse
              faculty {
                id
              }
              grades {
                id
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

    res_json = content.get("data").get(operation_name).get("objects")
    all_lecturers = Lecturer.objects.all()
    for lecturer in res_json:
        expected_lecturer = all_lecturers.get(id=lecturer.get("id"))
        assert lecturer.get("id") == str(expected_lecturer.id)
        assert lecturer.get("courses") == list(expected_lecturer.course_set.all())
        assert lecturer.get("username") == expected_lecturer.username
        assert lecturer.get("email") == expected_lecturer.email
        assert lecturer.get("name") == expected_lecturer.name
        assert lecturer.get("indexCode") == expected_lecturer.index_code


@pytest.mark.django_db
def test_get_lecturer_by_id_query(client_query, simple_lecturers):
    lecturer = simple_lecturers[-1]
    operation_name = "lecturerById"
    response = client_query(
        """
        query lecturerById ($id: String!) {
          lecturerById (id: $id) {
            id
            indexCode
            name
            email
            username
            courses {
              id
              name
              courseCode
              courseKind
              ectsForCourse
              faculty {
                id
                name
              }
              grades {
                id
                value
                isFinalGrade
                obtainedBy {
                  id
                  name
                }
                providedBy {
                  id
                  name
                }
              }
            }
          }
        }
        """,
        op_name=operation_name,
        variables={"id": lecturer.id},
    )
    content = json.loads(response.content)
    assert "errors" not in content

    result = content.get("data").get(operation_name)

    assert result.get("id") == str(lecturer.id)
    assert result.get("courses") == list(lecturer.course_set.all())
    assert result.get("username") == lecturer.username
    assert result.get("email") == lecturer.email
    assert result.get("name") == lecturer.name
    assert result.get("indexCode") == lecturer.index_code
