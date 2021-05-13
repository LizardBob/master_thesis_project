from typing import Any, List, Optional

from django.core.management.base import BaseCommand

from student_system_service.conftest import faculty_factory, lecturer_factory
from student_system_service.courses.consts import CourseType
from student_system_service.courses.models import Course
from student_system_service.grades.const import GradeValue
from student_system_service.grades.models import Grade
from student_system_service.students.models import Faculty, Student
from student_system_service.users.models import Lecturer, User


class Command(BaseCommand):
    help = "Generate Fake Data For Student System Service"
    course_type_mapping = {
        "0": CourseType.LECTURE,
        "1": CourseType.LABORATORY,
        "2": CourseType.SEMINARY,
    }

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write("\tHellothere!")
        self.cleanup_db()
        self.stdout.write("Clean Up Done\n")

        lecturers = self.create_lectures()
        self.stdout.write("Created Lecturers")

        faculties = self.create_faculties(quantity=3)
        self.stdout.write("Created Faculties")

        self.create_students(faculties[0])
        self.stdout.write("Created Students")

        for index, lecturer in enumerate(lecturers):
            self.create_courses(
                faculties[0], lecturer, self.course_type_mapping.get(str(index))
            )
        self.stdout.write("Created Courses")

        self.create_course_grades_for_student(lecturers[0])
        self.stdout.write("Created Grades")

        self.create_superuser()
        self.stdout.write("Created My Account")

        return "finish"

    def cleanup_db(self):
        Student.objects.all().delete()
        Grade.objects.all().delete()
        Course.objects.all().delete()
        Faculty.objects.all().delete()
        Lecturer.objects.all().delete()
        User.objects.all().delete()

    def create_lectures(self):
        return lecturer_factory(3)

    def create_faculties(self, quantity=3):
        faculties_list = []
        for i in range(quantity):
            faculty = faculty_factory(f"Test Faculty {i + 1}")
            faculties_list.append(faculty)
        return faculties_list

    def create_students(self, simple_faculty, quantity=2):
        for i in range(quantity):
            Student.objects.create(
                username=f"TestStudent_{i}",
                email=f"student{i}.test@test.com",
                password="123",
                faculty=simple_faculty,
            )

    def create_courses(self, faculty, lecturer, course_type, quantity=3):
        for i in range(quantity):
            Course.objects.create(
                name=f"Test Course {i}",
                course_type=course_type,
                ects_for_course=2,
                faculty=faculty,
                lecturer=lecturer,
            )

    def create_course_grades_for_student(self, lecturer):
        grades_values: List[str] = [
            value[0] for value in GradeValue.GRADE_VALUES_CHOICES
        ]
        students = Student.objects.all()
        courses = Course.objects.all()

        for grade_value in grades_values:
            for student in students:
                for course in courses:
                    course.student_set.add(student)
                    grade = Grade.objects.create(
                        value=grade_value,
                        is_final_grade=False,
                        obtained_by=student,
                        provided_by=lecturer,
                    )
                    course.grades.add(grade)

    def create_superuser(self) -> User:
        return User.objects.create_superuser(
            "lizard", "lizard@example.com", "123qweASD"
        )
