from typing import List, Union

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


def grade_factory(simple_student) -> Grade:
    return Grade.objects.create(
        value=GradeValue.AVERAGE, is_final_grade=False, obtained_by=simple_student
    )


def course_factory(
    course_name: str,
    simple_faculty: Faculty,
    grade_factory: Grade,
    simple_student: Student,
    simple_lecturer: Lecturer,
    quantity=1,
) -> Union[Course, List[Course]]:
    if quantity == 1:
        course = Course.objects.create(
            name=course_name,
            course_type=CourseType.LECTURE,
            ects_for_course=2,
            faculty=simple_faculty,
            lecturer=simple_lecturer,
        )
        course.grades.set([grade_factory])
        course.student_set.set([simple_student])
        return course
    courses_list: List[Course] = []

    for i in range(quantity):
        courses_list.append(
            Course.objects.create(
                name=f"{course_name}_{i}",
                course_type=CourseType.LECTURE,
                ects_for_course=2,
                faculty=simple_faculty,
                lecturer=simple_lecturer,
            )
        )

    for course in courses_list:
        course.grades.set([grade_factory])
        course.student_set.set([simple_student])

    return courses_list


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def simple_grade(simple_student) -> Grade:
    return grade_factory(simple_student)


@pytest.fixture
def simple_faculty() -> Faculty:
    return faculty_factory("Test Faculty")


def student_factory(simple_faculty, quantity=1) -> Union[Student, List[Student]]:
    if quantity == 1:
        return Student.objects.create(
            username="TestStudent",
            email="student.test@test.com",
            password="123",
            faculty=simple_faculty,
        )
    students_list: List[Student] = []
    for i in range(quantity):
        instance = Student.objects.create(
            username=f"TestStudent_{i}",
            email=f"student{i}.test@test.com",
            password="123",
            faculty=simple_faculty,
        )
        students_list.append(instance)

    return students_list


@pytest.fixture
def simple_student(simple_faculty) -> Student:
    return student_factory(simple_faculty)


@pytest.fixture
def simple_students(simple_faculty) -> List[Student]:
    return student_factory(simple_faculty, quantity=3)


@pytest.fixture
def simple_course(
    simple_faculty, simple_grade, simple_student, simple_lecturer
) -> Course:
    return course_factory(
        "TestCourse", simple_faculty, simple_grade, simple_student, simple_lecturer
    )


@pytest.fixture
def simple_courses(
    simple_faculty, simple_grade, simple_student, simple_lecturer
) -> List[Course]:
    return course_factory(
        "TestCourse",
        simple_faculty,
        simple_grade,
        simple_student,
        simple_lecturer,
        quantity=3,
    )


def lecturer_factory(quantity=1):
    if quantity == 1:
        return Lecturer.objects.create(
            username="TestLecturer",
            email="lecturer.test@test.com",
            password="123",
        )
    lecturers_list: List[Lecturer] = []
    for i in range(quantity):
        lecturer = Lecturer.objects.create(
            username=f"TestLecturer_{i}",
            email=f"lecturer{i}.test@test.com",
            password="123",
        )
        lecturers_list.append(lecturer)

    return lecturers_list


@pytest.fixture
def simple_lecturer() -> Lecturer:
    return lecturer_factory()


@pytest.fixture
def simple_lecturers() -> List[Lecturer]:
    return lecturer_factory(quantity=3)
