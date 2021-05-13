import json

import pytest
from django.urls import resolve, reverse
from rest_framework import status

from student_system_service.users.models import Lecturer, User

pytestmark = pytest.mark.django_db


def test_user_detail(user: User):
    url = reverse("api:user-detail", kwargs={"username": user.username})
    assert url == f"/v1/api/users/{user.username}/"
    assert resolve(f"/v1/api/users/{user.username}/").view_name == "api:user-detail"


def test_user_list():
    assert reverse("api:user-list") == "/v1/api/users/"
    assert resolve("/v1/api/users/").view_name == "api:user-list"


def test_user_me():
    assert reverse("api:user-me") == "/v1/api/users/me/"
    assert resolve("/v1/api/users/me/").view_name == "api:user-me"


@pytest.mark.django_db
def test_get_lecturers_list_view(api_client, simple_lecturers):
    url = reverse("api:lecturer-list")
    response = api_client.get(url)
    res_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(res_json) == Lecturer.objects.count()
    all_lecturers = Lecturer.objects.all()

    for lecturer in res_json:
        expected_lecturer = all_lecturers.get(id=lecturer.get("id"))
        assert lecturer.get("id") == expected_lecturer.id
        assert lecturer.get("courses") == list(expected_lecturer.course_set.all())
        assert lecturer.get("password") == expected_lecturer.password  # TODO remove it
        assert lecturer.get("username") == expected_lecturer.username
        assert lecturer.get("email") == expected_lecturer.email
        assert lecturer.get("name") == expected_lecturer.name
        assert lecturer.get("index_code") == expected_lecturer.index_code


@pytest.mark.django_db
def test_create_lecturer_view(api_client, simple_lecturers):
    url = reverse("api:lecturer-list")
    data = {
        "password": "123",
        "username": "Lect_Test",
        "email": "lecTest@test.com",
        "name": "K Drapa",
    }
    response = api_client.post(
        url, data=json.dumps(data), content_type="application/json"
    )
    res_json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    new_lecturer = Lecturer.objects.last()

    assert res_json.get("id") == new_lecturer.id
    assert res_json.get("courses") == list(new_lecturer.course_set.all())
    assert res_json.get("password") == new_lecturer.password  # TODO remove that
    assert res_json.get("username") == new_lecturer.username
    assert res_json.get("email") == new_lecturer.email
    assert res_json.get("name") == new_lecturer.name
    assert res_json.get("index_code") == new_lecturer.index_code


@pytest.mark.django_db
def test_update_lecturer_view(api_client, simple_lecturers):
    updating_lecturer = simple_lecturers[0]
    url = reverse("api:lecturer-detail", args=[updating_lecturer.id])
    data = {
        "password": "432",
        "username": "TestLec",
        "email": "TestLec@test.com",
        "name": "DrapaK",
    }
    assert updating_lecturer.password != data.get("password")
    assert updating_lecturer.username != data.get("username")
    assert updating_lecturer.email != data.get("email")
    assert updating_lecturer.name != data.get("name")

    response = api_client.put(url, data=data, content_type="application/json")
    res_json = response.json()
    updating_lecturer.refresh_from_db()

    assert updating_lecturer.password != res_json.get("password")
    assert updating_lecturer.username != res_json.get("username")
    assert updating_lecturer.email != res_json.get("email")
    assert updating_lecturer.name != res_json.get("name")


@pytest.mark.django_db
def test_delete_lecturer_view(api_client, simple_lecturers):
    deleting_lecturer = simple_lecturers[-1]
    url = reverse("api:lecturer-detail", args=[deleting_lecturer.id])
    response = api_client.delete(url, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
