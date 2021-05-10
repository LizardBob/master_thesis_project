from ..conftest import *  # noqa
from student_system_service.courses.consts import CourseType


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
