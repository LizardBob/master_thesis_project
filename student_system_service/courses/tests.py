from ..conftest import *  # noqa
from student_system_service.courses.consts import CourseType


@pytest.mark.django_db
def test_course_model_create(simple_course, simple_faculty, simple_grade):
    assert simple_course.name == "TestCourse"
    assert simple_course.course_code == "c0001"
    assert simple_course.course_type == CourseType.LECTURE
    assert simple_course.ects_for_course == 2
    assert simple_course.faculty == simple_faculty
    assert simple_course.grades.exists()
    assert simple_course.grades.count() == Grade.objects.count()
    assert [i.id for i in simple_course.grades.all()] == [
        i.id for i in Grade.objects.all()
    ]
    assert simple_course.student_set.exists()
