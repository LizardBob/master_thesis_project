import json

import environ
import requests

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


class GenerateRequestCallMixin:
    def __init__(self):
        self.token = self.call_for_token()

    def call_for_token(self):
        url = "http://localhost:8000/auth-token/"
        payload = {"username": env("ADMIN_USER"), "password": env("ADMIN_PASS")}
        headers = {
            "cookie": "csrftoken=wIfF4QGqdXTH4rzh6DU3U66Q5wwObAXebIHXEwGz9pCMArwXE46d1yMC8rBams5g",
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        return json.loads(response.text).get("token")
