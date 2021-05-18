from typing import Any, Optional

from django.core.management.base import BaseCommand

from student_system_service.courses.models import Course, Faculty
from student_system_service.students.models import Student
from student_system_service.users.models import Lecturer

from ...factories import (
    CourseFactory,
    FacultyFactory,
    GradeFactory,
    LecturerFactory,
    StudentFactory,
)
from .fakedata import Command as FakeDataCommand


class Command(BaseCommand):
    help = "Command for filling db with fakedata"
    NUMBER_OF_STUDENTS_PER_LEVEL = {
        "level_1": 1000,
        "level_2": 10000,
        "level_3": 100000,
    }
    number_of_students = 0

    def add_arguments(self, parser):
        parser.add_argument(
            "--level_1", action="store_true", help="Level of amount of db records"
        )
        parser.add_argument(
            "--level_2", action="store_true", help="Level of amount of db records"
        )
        parser.add_argument(
            "--level_3", action="store_true", help="Level of amount of db records"
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        FakeDataCommand().cleanup_db()
        FakeDataCommand().create_superuser()
        self.stdout.write("Elo it is it!")
        if options.get("--level_1", True):  # TODO change
            self.number_of_students = self.NUMBER_OF_STUDENTS_PER_LEVEL.get("level_1")
            self.fill_db_for_level_1()

        self.stdout.write(self.style.SUCCESS("Finished"))

    def fill_db_for_level_1(
        self,
        number_of_faculties=5,
        number_of_lecturers=15,
        number_of_courses=28,
        number_of_grades_per_course=5,
        number_of_students_per_fauclty=20,
    ):
        for i in range(number_of_faculties):
            FacultyFactory()

        faculties = Faculty.objects.all()
        for faculty in faculties:
            for i in range(number_of_students_per_fauclty):
                StudentFactory.create(faculty=faculty)

        assert Student.objects.count() == 100
        for i in range(number_of_lecturers):
            LecturerFactory()

        lecturers = Lecturer.objects.all()

        multiple_faculty = 1
        multiple_lecturer = 1

        for i in range(number_of_courses):
            faculty_number, multiple_faculty = self.handle_index_of_smaller_array(
                i, number_of_faculties, multiple_faculty
            )
            lecturer_number, multiple_lecturer = self.handle_index_of_smaller_array(
                i, number_of_lecturers, multiple_lecturer
            )

            CourseFactory.create(
                faculty=faculties[faculty_number], lecturer=lecturers[lecturer_number]
            )
        assert Course.objects.count() == number_of_courses
        courses = Course.objects.all()
        students = Student.objects.all()
        self.stdout.write("Generating grades ")
        for course in courses:
            for student in students:
                course.student_set.add(student)
                for _ in range(number_of_grades_per_course):
                    grade = GradeFactory.create(
                        obtained_by_id=student.id, provided_by_id=course.lecturer_id
                    )
                    course.grades.add(grade)

    def handle_index_of_smaller_array(self, index, max_number, multiply_helper):
        if index >= max_number:
            possible_index = abs(index - multiply_helper * max_number)
            if possible_index == 0:
                multiply_helper += 1
        else:
            possible_index = index
        return possible_index, multiply_helper
