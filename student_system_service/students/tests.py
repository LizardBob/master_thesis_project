import json

import pytest
from django.urls import reverse
from rest_framework import status

from ..conftest import faculty_factory
from .models import Student


@pytest.mark.django_db
def test_student_model_create(simple_students, simple_faculty):
    for index, simple_student in enumerate(simple_students):
        assert simple_student.username == f"TestStudent_{index}"
        assert simple_student.email == f"student{index}.test@test.com"
        assert simple_student.faculty == simple_faculty
        assert simple_student.index_code == f"s{index + 1}"


@pytest.mark.django_db
def test_get_student_list_view(api_client, simple_students):
    url = reverse("api:student-list")
    response = api_client.get(url, content_type="application/json")
    res_json = response.json()
    assert response.status_code == status.HTTP_200_OK

    assert len(res_json) == Student.objects.count()
    all_students = Student.objects.all()

    for student in res_json:
        excpected_student = all_students.get(id=student.get("id"))
        assert (
            student.get("password") == excpected_student.password
        )  # TODO password should not be returned
        assert student.get("username") == excpected_student.username
        assert student.get("email") == excpected_student.email
        assert student.get("name") == excpected_student.name
        assert student.get("faculty") == excpected_student.faculty.id
        assert student.get("courses") == list(excpected_student.courses.all())


@pytest.mark.django_db
def test_create_student_view(api_client, simple_students, simple_faculty):
    url = reverse("api:student-list")
    data = {
        "password": "123",
        "username": "StS",
        "email": "ste@example.com",
        "name": "Ste",
        "faculty": simple_faculty.id,
        "courses": [],
    }
    response = api_client.post(
        url, data=json.dumps(data), content_type="application/json"
    )
    res_json = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    new_student = Student.objects.last()
    assert res_json.get("id") == new_student.id
    assert new_student.password == res_json.get("password")
    assert new_student.username == res_json.get("username")
    assert new_student.email == res_json.get("email")
    assert new_student.name == res_json.get("name")
    assert new_student.faculty.id == res_json.get("faculty")
    assert list(new_student.courses.all()) == res_json.get("courses")


@pytest.mark.django_db
def test_update_student_view(
    api_client, simple_students, simple_faculty, simple_courses
):
    new_faculty = faculty_factory("New Test Faculty")
    updating_student = simple_students[0]
    url = reverse("api:student-detail", args=[updating_student.id])
    data = {
        "password": "432",
        "username": "StS",
        "email": "ste@example.com",
        "name": "Ste",
        "faculty": new_faculty.id,
        "courses": [simple_courses[0].id],
    }

    assert updating_student.password != data.get("password")
    assert updating_student.username != data.get("username")
    assert updating_student.email != data.get("email")
    assert updating_student.name != data.get("name")
    assert updating_student.faculty.id != data.get("faculty")
    assert list(updating_student.courses.all()) != data.get("courses")

    response = api_client.put(
        url, data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    updating_student.refresh_from_db()
    assert updating_student.id == res_json.get("id")
    assert updating_student.password == res_json.get("password")
    assert updating_student.username == res_json.get("username")
    assert updating_student.email == res_json.get("email")
    assert updating_student.name == res_json.get("name")
    assert updating_student.faculty.id == res_json.get("faculty")
    assert list(updating_student.courses.values_list("id", flat=True)) == res_json.get(
        "courses"
    )


@pytest.mark.django_db
def test_delete_student_view(api_client, simple_students, simple_courses):
    deleting_student = simple_students[-1]
    url = reverse("api:student-detail", args=[deleting_student.id])
    response = api_client.delete(url, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
