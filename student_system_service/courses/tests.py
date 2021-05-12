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
