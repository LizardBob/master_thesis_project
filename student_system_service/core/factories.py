import factory
from factory import fuzzy
from faker import Faker

from student_system_service.courses.consts import CourseTypes
from student_system_service.courses.models import Course, Faculty
from student_system_service.grades.const import GradeValue
from student_system_service.grades.models import Grade
from student_system_service.students.models import Student
from student_system_service.users.models import Lecturer

fake = Faker()
course_types_ids = [x[0] for x in CourseTypes.COURSE_TYPE_CHOICES]
grades_values = [x[0] for x in GradeValue.GRADE_VALUES_CHOICES]


class FacultyFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(
        lambda x: f"{fake.job()} {fake.linux_processor()} {fake.prefix()}"
    )

    class Meta:
        model = Faculty


class StudentFactory(factory.django.DjangoModelFactory):
    password = fuzzy.FuzzyText(length=9)
    username = fuzzy.FuzzyText(length=12)
    email = factory.LazyAttribute(lambda x: fake.ascii_safe_email())
    name = factory.LazyAttribute(lambda x: fake.first_name())
    faculty = factory.SubFactory(FacultyFactory)

    class Meta:
        model = Student


class LecturerFactory(factory.django.DjangoModelFactory):
    password = fuzzy.FuzzyText(length=9)
    username = fuzzy.FuzzyText(length=12)
    email = factory.LazyAttribute(lambda x: f"{fake.prefix()}{fake.ascii_safe_email()}")
    name = factory.LazyAttribute(lambda x: f"{fake.prefix()}{fake.first_name()}")

    class Meta:
        model = Lecturer


class CourseFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda x: f"{fake.catch_phrase()}")
    course_kind = fuzzy.FuzzyChoice(course_types_ids)
    ects_for_course = fuzzy.FuzzyInteger(1, 10)

    class Meta:
        model = Course


class GradeFactory(factory.django.DjangoModelFactory):
    value = fuzzy.FuzzyChoice(grades_values)
    is_final_grade = False

    class Meta:
        model = Grade
