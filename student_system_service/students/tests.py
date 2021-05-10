from ..conftest import *  # noqa


@pytest.mark.django_db
def test_student_model_create(simple_student, simple_faculty):
    assert simple_student.username == "TestStudent"
    assert simple_student.email == "student.test@test.com"
    assert simple_student.faculty == simple_faculty
    assert simple_student.index_code == "s001"  # TODO move it to save()
