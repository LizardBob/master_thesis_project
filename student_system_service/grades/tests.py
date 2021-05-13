import json

import pytest

from student_system_service.grades.const import GradeValue
from student_system_service.grades.models import Grade

from ..conftest import *  # noqa


@pytest.mark.django_db
def test_grade_model_create(simple_grade, simple_student):
    assert simple_grade.value == GradeValue.AVERAGE
    assert not simple_grade.is_final_grade
    assert simple_grade.obtained_by == simple_student


@pytest.mark.django_db
def test_get_all_grades(client_query, simple_grades):
    operation_name = "allGrades"
    response = client_query(
        """
        query allGrades {
          allGrades {
            obtainedBy {
              id
              name
              username
            }
            providedBy {
              id
              indexCode
              name
              username
            }
            value
            isFinalGrade
            id
          }
        }
        """,
        op_name=operation_name,
    )

    content = json.loads(response.content)
    assert "errors" not in content

    res_json = content.get("data").get(operation_name)
    all_grades = Grade.objects.all()
    for grade in res_json:
        expected_grade = all_grades.get(id=grade.get("id"))
        assert grade.get("id") == str(expected_grade.id)
        assert grade.get("value") == expected_grade.value
        assert grade.get("isFinalGrade") == expected_grade.is_final_grade
        obtained_by = grade.get("obtainedBy")
        provided_by = grade.get("providedBy")

        assert obtained_by.get("id") == str(expected_grade.obtained_by_id)
        assert obtained_by.get("name") == expected_grade.obtained_by.name
        assert obtained_by.get("username") == expected_grade.obtained_by.username
        assert provided_by.get("id") == str(expected_grade.provided_by.id)
        assert provided_by.get("name") == expected_grade.provided_by.name
        assert provided_by.get("username") == expected_grade.provided_by.username
        assert provided_by.get("indexCode") == expected_grade.provided_by.index_code


@pytest.mark.django_db
def test_get_grade_by_id(client_query, simple_grades):
    grade = simple_grades[-1]
    operation_name = "gradeById"
    response = client_query(
        """
        query gradeById($id: String!) {
          gradeById(id: $id) {
            obtainedBy {
              id
              name
              username
            }
            providedBy {
              id
              indexCode
              name
              username
            }
            value
            isFinalGrade
            id
          }
        }
        """,
        op_name=operation_name,
        variables={"id": grade.id},
    )
    content = json.loads(response.content)
    assert "errors" not in content

    result = content.get("data").get(operation_name)

    assert result.get("id") == str(grade.id)
    assert result.get("value") == grade.value
    assert result.get("isFinalGrade") == grade.is_final_grade
    obtained_by = result.get("obtainedBy")
    provided_by = result.get("providedBy")

    assert obtained_by.get("id") == str(grade.obtained_by_id)
    assert obtained_by.get("name") == grade.obtained_by.name
    assert obtained_by.get("username") == grade.obtained_by.username
    assert provided_by.get("id") == str(grade.provided_by.id)
    assert provided_by.get("name") == grade.provided_by.name
    assert provided_by.get("username") == grade.provided_by.username
    assert provided_by.get("indexCode") == grade.provided_by.index_code
