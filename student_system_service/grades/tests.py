from ..conftest import *


@pytest.mark.django_db
def test_grade_model_create(simple_grade, simple_student):
    assert simple_grade.value == GradeValue.AVERAGE
    assert not simple_grade.is_final_grade
    assert simple_grade.obtained_by == simple_student
