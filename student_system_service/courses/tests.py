import json

import pytest
from django.urls import reverse
from rest_framework import status

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
def test_get_faculties_list_view(api_client, simple_faculties):
    url = reverse("api:faculty-list")
    response = api_client.get(url)
    res_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(res_json) == Faculty.objects.count()

    faculties = Faculty.objects.all()
    for faculty in res_json:
        expected_faculty = faculties.get(id=faculty.get("id"))
        assert faculty.get("id") == expected_faculty.id
        assert faculty.get("name") == expected_faculty.name


@pytest.mark.django_db
def test_create_faculty_view(api_client, simple_faculties):
    url = reverse("api:faculty-list")
    data = {
        "name": "New Test Faculty",
    }
    response = api_client.post(
        url, data=json.dumps(data), content_type="application/json"
    )

    res_json = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    new_faculty = Faculty.objects.last()
    assert res_json.get("id") == new_faculty.id
    assert res_json.get("name") == new_faculty.name


@pytest.mark.django_db
def test_update_faculty_view(api_client, simple_faculties):
    updating_faculty = simple_faculties[0]
    url = reverse("api:faculty-detail", args=[updating_faculty.id])
    data = {
        "name": "Update Name",
    }
    assert updating_faculty.name != data.get("name")

    response = api_client.put(
        url, data=json.dumps(data), content_type="application/json"
    )
    res_json = response.json()
    updating_faculty.refresh_from_db()

    assert updating_faculty.id == res_json.get("id")
    assert updating_faculty.name == res_json.get("name")


@pytest.mark.django_db
def test_delete_faculty_view(api_client, simple_faculties):
    deleting_faculty = simple_faculties[-1]
    url = reverse("api:faculty-detail", args=[deleting_faculty.id])
    response = api_client.delete(url, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_get_courses_list_view(api_client, simple_courses):
    url = reverse("api:course-list")
    response = api_client.get(url, content_type="application/json")
    res_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(res_json) == Course.objects.count()

    all_courses = Course.objects.all()

    for course in res_json:
        expected_course = all_courses.get(id=course.get("id"))
        assert course.get("id") == expected_course.id
        assert course.get("name") == expected_course.name
        assert course.get("course_code") == expected_course.course_code
        assert course.get("course_type") == expected_course.course_type
        assert course.get("ects_for_course") == expected_course.ects_for_course
        assert course.get("faculty") == expected_course.faculty_id
        assert course.get("lecturer") == expected_course.lecturer_id
        assert course.get("grades") == list(
            expected_course.grades.values_list("id", flat=True)
        )


@pytest.mark.django_db
def test_create_course_view(
    api_client, simple_courses, simple_faculties, simple_lecturers
):
    faculty = simple_faculties[0]
    lecturer = simple_lecturers[0]
    url = reverse("api:course-list")
    data = {
        "name": "New Course Programming",
        "course_type": "laboratory",
        "ects_for_course": 2,
        "faculty": faculty.id,
        "lecturer": lecturer.id,
        "grades": [],
    }
    response = api_client.post(
        url, data=json.dumps(data), content_type="application/json"
    )
    res_json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    new_course = Course.objects.last()
    assert res_json.get("id") == new_course.id
    assert res_json.get("name") == new_course.name
    assert res_json.get("course_code") == new_course.course_code
    assert res_json.get("course_type") == new_course.course_type
    assert res_json.get("ects_for_course") == new_course.ects_for_course
    assert res_json.get("faculty") == new_course.faculty_id
    assert res_json.get("lecturer") == new_course.lecturer_id
    assert res_json.get("grades") == list(new_course.grades.all())


@pytest.mark.django_db
def test_update_course_view(
    api_client, simple_courses, simple_faculties, simple_lecturers, simple_grade
):
    updating_course = simple_courses[0]
    url = reverse("api:course-detail", args=[updating_course.id])
    data = {
        "name": "New Course Programming",
        "course_type": "seminary",
        "ects_for_course": 4,
        "faculty": simple_faculties[-1].id,
        "lecturer": simple_lecturers[-1].id,
        "grades": [simple_grade.id],
    }
    assert updating_course.name != data.get("name")
    assert updating_course.course_type != data.get("course_type")
    assert updating_course.ects_for_course != data.get("ects_for_course")
    assert updating_course.faculty_id != data.get("faculty")
    assert updating_course.lecturer_id != data.get("lecturer")
    assert list(updating_course.grades.all()) != data.get("grades")

    response = api_client.put(
        url, data=json.dumps(data), content_type="application/json"
    )
    res_json = response.json()

    updating_course.refresh_from_db()
    assert updating_course.name == res_json.get("name")
    assert updating_course.course_type == res_json.get("course_type")
    assert updating_course.ects_for_course == res_json.get("ects_for_course")
    assert updating_course.faculty_id == res_json.get("faculty")
    assert updating_course.lecturer_id == res_json.get("lecturer")
    assert list(updating_course.grades.values_list("id", flat=True)) == res_json.get(
        "grades"
    )


@pytest.mark.django_db
def test_delete_course_view(api_client, simple_courses):
    deleting_course = simple_courses[-1]
    url = reverse("api:course-detail", args=[deleting_course.id])
    response = api_client.delete(url, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
