import pytest

from student_system_service.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_lecturer_model_create(simple_lecturer, simple_course):
    assert simple_lecturer.index_code == "lec0001"  # TODO move to save()
    assert simple_lecturer.courses == simple_course
    assert simple_lecturer.username == "TestLecturer"
    assert simple_lecturer.email == "lecturer.test@test.com"
