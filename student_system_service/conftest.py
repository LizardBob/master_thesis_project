import pytest

from student_system_service.courses.consts import CourseType
from student_system_service.grades.const import GradeValue
from student_system_service.grades.models import Grade
from student_system_service.users.models import User, Lecturer
from student_system_service.users.tests.factories import UserFactory
from student_system_service.students.models import Student
from student_system_service.courses.models import Faculty, Course


def faculty_factory(faculty_name: str) -> Faculty:
    return Faculty.objects.create(name=faculty_name)


def grade_factory(simple_student):
    return Grade.objects.create(
        value=GradeValue.AVERAGE, is_final_grade=False, obtained_by=simple_student
    )


def course_factory(course_name: str, simple_faculty, grade_factory, simple_student) -> Course:
    course = Course.objects.create(
        name=course_name,
        course_code="c0001",  # TODO change it move to save()
        course_type=CourseType.LECTURE,
        ects_for_course=2,
        faculty=simple_faculty,
    )
    course.grades.set([grade_factory])
    course.student_set.set([simple_student])
    return course


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def simple_grade(simple_student):
    return grade_factory(simple_student)


@pytest.fixture
def simple_faculty():
    return faculty_factory("Test Faculty")


def student_factory(simple_faculty) -> Student:
    return Student.objects.create(
        username="TestStudent",
        email="student.test@test.com",
        password="123",
        faculty=simple_faculty,
        index_code="s001",
    )

@pytest.fixture
def simple_student(simple_faculty) -> Student:
    return student_factory(simple_faculty)


@pytest.fixture
def simple_course(simple_faculty, simple_grade, simple_student):
    return course_factory("TestCourse", simple_faculty, simple_grade, simple_student)


@pytest.fixture
def simple_lecturer(simple_course) -> Lecturer:
    return Lecturer.objects.create(
        username="TestLecturer",
        email="lecturer.test@test.com",
        password="123",
        index_code="lec0001",
        courses=simple_course,
    )
