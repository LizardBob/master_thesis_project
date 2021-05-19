import json

import pytest

from student_system_service.courses.consts import CourseTypes
from student_system_service.courses.models import Course, Faculty
from student_system_service.grades.models import Grade

from ..conftest import *  # noqa


@pytest.mark.django_db
def test_course_model_create(simple_courses, simple_faculty, simple_grade):
    for index, simple_course in enumerate(simple_courses):
        assert simple_course.name == f"TestCourse_{index}"
        assert simple_course.course_code == f"c{index + 1}"
        assert simple_course.course_kind == CourseTypes.LECTURE
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


@pytest.mark.django_db
def test_get_all_courses_query(client_query, simple_courses):
    operation_name = "allCourses"
    response = client_query(
        """
        query allCourses {
          allCourses (page: 1) {
            page
            pages
            hasNext
            hasPrev
            objects {
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
                value
                obtainedBy {
                  id
                  username
                }
                id
              }
              lecturer {
                id
                name
                username
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
    all_courses = Course.objects.all()

    for course in res_json:
        expected_course = all_courses.get(id=course.get("id"))
        assert course.get("id") == str(expected_course.id)
        assert course.get("name") == expected_course.name
        assert course.get("courseCode") == expected_course.course_code
        assert course.get("courseKind") == expected_course.course_kind.upper()
        assert course.get("ectsForCourse") == expected_course.ects_for_course
        faculty = course.get("faculty")
        lecturer = course.get("lecturer")

        assert faculty.get("id") == str(expected_course.faculty_id)
        assert faculty.get("name") == expected_course.faculty.name
        assert len(course.get("grades")) == len(
            list(expected_course.grades.values_list("id", flat=True))
        )
        assert lecturer.get("id") == str(expected_course.lecturer_id)
        assert lecturer.get("name") == expected_course.lecturer.name
        assert lecturer.get("username") == expected_course.lecturer.username
        grades = course.get("grades")
        for grade in grades:
            expected_grade = expected_course.grades.get(id=grade.get("id"))
            obtained_by = grade.get("obtainedBy")

            assert grade.get("id") == str(expected_grade.id)
            assert grade.get("value") == expected_grade.value
            assert obtained_by.get("id") == str(expected_grade.obtained_by_id)
            assert obtained_by.get("username") == expected_grade.obtained_by.username


@pytest.mark.django_db
def test_get_course_by_id(client_query, simple_courses):
    course = simple_courses[-1]
    operation_name = "courseById"
    response = client_query(
        """
        query courseById ($id: String!) {
          courseById (id: $id) {
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
              value
              obtainedBy {
                id
                username
              }
              id
            }
            lecturer {
              id
              name
              username
            }
          }
        }
        """,
        op_name=operation_name,
        variables={"id": course.id},
    )

    content = json.loads(response.content)
    assert "errors" not in content

    result = content.get("data").get(operation_name)

    assert result.get("id") == str(course.id)
    assert result.get("name") == course.name
    assert result.get("courseCode") == course.course_code
    assert result.get("courseKind") == course.course_kind.upper()
    assert result.get("ectsForCourse") == course.ects_for_course
    faculty = result.get("faculty")
    lecturer = result.get("lecturer")

    assert faculty.get("id") == str(course.faculty_id)
    assert faculty.get("name") == course.faculty.name
    assert len(result.get("grades")) == len(
        list(course.grades.values_list("id", flat=True))
    )
    assert lecturer.get("id") == str(course.lecturer_id)
    assert lecturer.get("name") == course.lecturer.name
    assert lecturer.get("username") == course.lecturer.username
    grades = result.get("grades")
    for grade in grades:
        expected_grade = course.grades.get(id=grade.get("id"))
        obtained_by = grade.get("obtainedBy")

        assert grade.get("id") == str(expected_grade.id)
        assert grade.get("value") == expected_grade.value
        assert obtained_by.get("id") == str(expected_grade.obtained_by_id)
        assert obtained_by.get("username") == expected_grade.obtained_by.username


@pytest.mark.django_db
def test_create_faculty_mutation(client_query, simple_faculties):
    operation_name = "createFaculty"
    data = {
        "name": "New Test Faculty",
    }
    response = client_query(
        """
        mutation createFaculty($input: FacultyInput!) {
          createFaculty(inputData: $input) {
            faculty{
              id
              name
            }
          }
        }
        """,
        op_name=operation_name,
        input_data=data,
    )

    content = json.loads(response.content)
    assert "errors" not in content

    res_json = content.get("data").get(operation_name).get("faculty")
    assert Faculty.objects.count() == 4
    new_faculty = Faculty.objects.last()
    assert res_json.get("id") == f"{new_faculty.id}"
    assert res_json.get("name") == new_faculty.name


@pytest.mark.django_db
def test_update_faculty_mutation(client_query, simple_faculties):
    updating_faculty = simple_faculties[-1]
    operation_name = "updateFaculty"
    data = {
        "id": updating_faculty.id,
        "name": "Databases with MVC",
    }
    response = client_query(
        """
        mutation updateFaculty($input: FacultyUpdateMutationInput!) {
          updateFaculty(input: $input) {
            id
            name
          }
        }
        """,
        op_name=operation_name,
        input_data=data,
    )

    content = json.loads(response.content)

    assert "errors" not in content
    updating_faculty.refresh_from_db()
    res_json = content.get("data").get(operation_name)

    updating_faculty.refresh_from_db()

    assert updating_faculty.id == res_json.get("id")
    assert updating_faculty.name == res_json.get("name")


@pytest.mark.django_db
def test_delete_faculty_mutation(client_query, simple_faculties):
    deleting_faculty = simple_faculties[-1]
    operation_name = "deleteFaculty"
    response = client_query(
        """
        mutation deleteFaculty($id: Int) {
          deleteFaculty(id: $id) {
            ok
          }
        }
        """,
        op_name=operation_name,
        variables={"id": deleting_faculty.id},
    )

    content = json.loads(response.content)
    assert "errors" not in content

    res_json = content.get("data").get(operation_name)
    assert res_json.get("ok")
    assert Faculty.objects.count() == 2


@pytest.mark.django_db
def test_create_course_mutation(
    client_query, simple_courses, simple_faculties, simple_lecturers
):
    faculty = simple_faculties[0]
    lecturer = simple_lecturers[0]
    operation_name = "createCourse"
    data = {
        "name": "New Course Programming",
        "courseKind": "laboratory",
        "ectsForCourse": 2,
        "faculty": faculty.id,
        "lecturer": lecturer.id,
        "grades": [],
    }
    response = client_query(
        """
        mutation createCourse($input: CourseInput!) {
          createCourse(inputData: $input) {
            course {
              id
              name
              courseKind
              courseCode
              ectsForCourse
              faculty {
                id
              }
              lecturer {
                id
              }
              grades{
                id
                isFinalGrade
                obtainedBy {
                  id
                }
                providedBy {
                  id
                }
                value
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

    res_json = content.get("data").get(operation_name).get("course")
    assert Course.objects.count() == 4
    new_course = Course.objects.last()

    assert res_json.get("id") == f"{new_course.id}"
    assert res_json.get("name") == new_course.name
    assert res_json.get("courseCode") == new_course.course_code
    assert res_json.get("courseKind") == new_course.course_kind.upper()
    assert res_json.get("ectsForCourse") == new_course.ects_for_course
    assert res_json.get("faculty").get("id") == f"{new_course.faculty_id}"
    assert res_json.get("lecturer").get("id") == f"{new_course.lecturer_id}"
    assert res_json.get("grades") == list(new_course.grades.all())


@pytest.mark.django_db
def test_update_course_mutation(
    client_query, simple_courses, simple_grade, simple_faculties, simple_lecturers
):
    updating_course = simple_courses[0]
    operation_name = "updateCourse"
    data = {
        "id": updating_course.id,
        "name": "New Course Programming",
        "courseKind": "seminary",
        "ectsForCourse": 4,
        "faculty": simple_faculties[-1].id,
        "lecturer": simple_lecturers[-1].id,
        "grades": [simple_grade.id],
    }

    response = client_query(
        """
        mutation updateCourse($input: CourseInput!) {
          updateCourse(inputData: $input) {
            course {
              id
              name
              courseCode
              courseKind
              ectsForCourse
              faculty {
                id
              }
              lecturer {
                id
              }
              grades{
                id
                isFinalGrade
                obtainedBy {
                  id
                }
                providedBy {
                  id
                }
                value
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

    res_json = content.get("data").get(operation_name).get("course")
    updating_course.refresh_from_db()

    assert updating_course.name == res_json.get("name")
    assert updating_course.course_kind.upper() == res_json.get("courseKind")
    assert updating_course.ects_for_course == res_json.get("ectsForCourse")
    assert f"{updating_course.faculty_id}" == res_json.get("faculty").get("id")
    assert f"{updating_course.lecturer_id}" == res_json.get("lecturer").get("id")
    assert len(list(updating_course.grades.values_list("id", flat=True))) == len(
        res_json.get("grades")
    )
    assert (
        f"{list(updating_course.grades.values_list('id', flat=True))[0]}"
        == res_json.get("grades")[0].get("id")
    )


@pytest.mark.django_db
def test_delete_course_mutation(client_query, simple_courses):
    deleting_course = simple_courses[-1]
    operation_name = "deleteCourse"
    response = client_query(
        """
        mutation deleteCourse($id: Int) {
          deleteCourse(id: $id) {
            ok
          }
        }
        """,
        op_name=operation_name,
        variables={"id": deleting_course.id},
    )
    content = json.loads(response.content)
    assert "errors" not in content

    res_json = content.get("data").get(operation_name)
    assert res_json.get("ok")
    assert Course.objects.count() == 2
