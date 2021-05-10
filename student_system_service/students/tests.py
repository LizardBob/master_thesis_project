from ..conftest import *  # noqa


@pytest.mark.django_db
def test_student_model_create(simple_students, simple_faculty):
    for index, simple_student in enumerate(simple_students):
        assert simple_student.username == f"TestStudent_{index}"
        assert simple_student.email == f"student{index}.test@test.com"
        assert simple_student.faculty == simple_faculty
        assert simple_student.index_code == f"s{index + 1}"
