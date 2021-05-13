import pytest

from student_system_service.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_lecturer_model_create(simple_lecturers, simple_course):
    for index, simple_lecturer in enumerate(simple_lecturers):
        assert simple_lecturer.index_code == f"lec{index + 1}"
        assert list(simple_lecturer.course_set.all()) != simple_course
        assert simple_lecturer.username == f"TestLecturer_{index}"
        assert simple_lecturer.email == f"lecturer{index}.test@test.com"
