from typing import List, Union

import pytest
from graphene_django.utils.testing import graphql_query
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from student_system_service.courses.consts import CourseTypes
from student_system_service.courses.models import Course, Faculty
from student_system_service.grades.const import GradeValue
from student_system_service.grades.models import Grade
from student_system_service.students.models import Student
from student_system_service.users.models import Lecturer, User
from student_system_service.users.tests.factories import UserFactory

# from pytest_django.fixtures import client


def faculty_factory(faculty_name: str, quantity=1) -> Union[Faculty, List[Faculty]]:
    if quantity == 1:
        return Faculty.objects.create(name=faculty_name)
    faculties_list: List[Faculty] = []
    for i in range(quantity):
        faculties_list.append(Faculty(name=f"{faculty_name}_{i + 1}"))

    Faculty.objects.bulk_create(faculties_list)
    return faculties_list


def grade_factory(
    simple_student, simple_lecturer, quantity=1
) -> Union[Grade, List[Grade]]:
    if quantity == 1:
        return Grade.objects.create(
            value=GradeValue.AVERAGE,
            is_final_grade=False,
            obtained_by=simple_student,
            provided_by=simple_lecturer,
        )
    grades_list: List[Grade] = []
    for i in range(quantity):
        grades_list.append(
            Grade(
                value=GradeValue.AVERAGE,
                is_final_grade=False,
                obtained_by=simple_student,
                provided_by=simple_lecturer,
            )
        )
    Grade.objects.bulk_create(grades_list)
    return grades_list


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
            course_kind=CourseTypes.LECTURE,
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
                course_kind=CourseTypes.LECTURE,
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
def get_or_create_token(db, simple_student):
    token, _ = Token.objects.get_or_create(user=simple_student)
    return token


@pytest.fixture
def api_client(get_or_create_token):
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {get_or_create_token}")
    return api_client


@pytest.fixture
def client_query(client):
    def prepare_query(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return prepare_query


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def simple_grade(simple_student, simple_lecturer) -> Grade:
    return grade_factory(simple_student, simple_lecturer)


@pytest.fixture
def simple_grades(simple_student, simple_lecturer) -> List[Grade]:
    return grade_factory(simple_student, simple_lecturer, quantity=3)


@pytest.fixture
def simple_faculty() -> Faculty:
    return faculty_factory("Test Faculty")


@pytest.fixture
def simple_faculties() -> Faculty:
    return faculty_factory("Test Faculty", quantity=3)


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
