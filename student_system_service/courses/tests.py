import json

import pytest

from student_system_service.courses.consts import CourseType
from student_system_service.courses.models import Faculty, Grade

from ..conftest import *  # noqa


@pytest.mark.django_db
def test_course_model_create(simple_courses, simple_faculty, simple_grade):
    for index, simple_course in enumerate(simple_courses):
        assert simple_course.name == f"TestCourse_{index}"
        assert simple_course.course_code == f"c{index + 1}"
        assert simple_course.course_type == CourseType.LECTURE
        assert simple_course.ects_for_course == 2
        assert simple_course.faculty == simple_faculty
        assert simple_course.grades.exists()
        assert simple_course.grades.count() == Grade.objects.count()
        assert [i.id for i in simple_course.grades.all()] == [
            i.id for i in Grade.objects.all()
        ]
        assert simple_course.student_set.exists()


@pytest.mark.django_db
def test_get_all_faculties_query(client_query, simple_faculties):
    operation_name = "allFaculties"
    response = client_query(
        """
        query allFaculties {
          allFaculties {
            id
            name
            students {
              id
              indexCode
            }
          }
        }
        """,
        op_name=operation_name,
    )

    content = json.loads(response.content)
    assert "errors" not in content
    res_json = content.get("data").get(operation_name)

    all_faculties = Faculty.objects.all()

    for faculty in res_json:
        expected_faculty = all_faculties.get(id=faculty.get("id"))
        assert faculty.get("id") == str(expected_faculty.id)
        assert faculty.get("name") == expected_faculty.name
        assert faculty.get("students") == list(expected_faculty.students.all())


@pytest.mark.django_db
def test_get_faculty_by_id_query(client_query, simple_faculties):
    faculty = simple_faculties[-1]
    operation_name = "facultyById"
    response = client_query(
        """
        query facultyById($id: String!) {
          facultyById(id: $id) {
            id
            name
            students {
              id
              username
              name
            }
          }
        }
        """,
        op_name=operation_name,
        variables={"id": faculty.id},
    )
    content = json.loads(response.content)
    assert "errors" not in content

    result = content.get("data").get(operation_name)

    assert result.get("id") == str(faculty.id)
    assert result.get("name") == faculty.name
    assert result.get("students") == list(faculty.students.all())
