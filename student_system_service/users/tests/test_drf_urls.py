import pytest
from django.urls import resolve, reverse

from student_system_service.users.models import User

pytestmark = pytest.mark.django_db


def test_user_detail(user: User):
    assert (
        reverse("api:user-detail", kwargs={"username": user.username})
        == f"/v1/api/users/{user.username}/"
    )
    assert resolve(f"/v1/api/users/{user.username}/").view_name == "api:user-detail"


def test_user_list():
    assert reverse("api:user-list") == "/v1/api/users/"
    assert resolve("/v1/api/users/").view_name == "api:user-list"


def test_user_me():
    assert reverse("api:user-me") == "/v1/api/users/me/"
    assert resolve("/v1/api/users/me/").view_name == "api:user-me"
