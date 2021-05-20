import environ

env = environ.Env()


# For Student
class StudentOperationName:
    FETCH_STUDENTS = "Fetch Students"
    CREATE_STUDENT = "Create Student"
    UPDATE_STUDENT = "Update Student"
    DELETE_STUDENT = "Delete Student"


# **** ****


class FacultyOperationName:
    FETCH_FACULTIES = "Fetch Faculties"
    CREATE_FACULTY = "Create Faculty"
    UPDATE_FACULTY = "Update Faculty"
    DELETE_FACULTY = "Delete Faculty"


# **** ****


class LecturerOperationName:
    FETCH_LECTURERS = "Fetch Lecturers"
    CREATE_LECTURER = "Create Lecturer"
    UPDATE_LECTURER = "Update Lecturer"
    DELETE_LECTURER = "Delete Lecturer"


# **** ****


class CourseOperationName:
    FETCH_COURSES = "Fetch Courses"
    CREATE_COURSE = "Create Course"
    UPDATE_COURSE = "Update Course"
    DELETE_COURSE = "Delete Course"


# **** ****


class GradeOperationName:
    FETCH_GRADES = "Fetch Grades"
    CREATE_GRADE = "Create Grade"
    UPDATE_GRADE = "Update Grade"
    DELETE_GRADE = "Delete Grade"
