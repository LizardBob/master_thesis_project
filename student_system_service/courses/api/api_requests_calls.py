import faker
import requests

from student_system_service.core.const import (
    CourseOperationName,
    FacultyOperationName,
    GenerateRequestCallMixin,
)
from student_system_service.courses.models import Faculty
from student_system_service.users.models import Lecturer

fake = faker.Faker()


class FacultyRequestCall(GenerateRequestCallMixin):
    SET_OF_REQUEST_VALUES = {
        FacultyOperationName.FETCH_FACULTIES: {},
        FacultyOperationName.CREATE_FACULTY: {},
        FacultyOperationName.UPDATE_FACULTY: {},
        FacultyOperationName.DELETE_FACULTY: {},
    }

    def run_and_collect(self):
        self.call_for_fetch_faculty()
        self.call_for_create_faculty()
        self.call_for_update_faculty()
        self.call_for_delete_faculty()

    def call_for_fetch_faculty(self):
        title = FacultyOperationName.FETCH_FACULTIES
        url = "http://localhost:8000/v1/api/faculty"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.request("GET", url, headers=headers)
        assert response.status_code == 200
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_faculty(self):
        title = FacultyOperationName.CREATE_FACULTY
        url = "http://localhost:8000/v1/api/faculty/"

        payload = {"name": f"{fake.job()}"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.token}",
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        assert response.status_code == 201
        self.update_instance_id = response.json().get("id")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True

    def call_for_update_faculty(self):
        title = FacultyOperationName.UPDATE_FACULTY
        url = f"http://localhost:8000/v1/api/faculty/{self.update_instance_id}/"

        payload = {"name": "W7"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.token}",
        }

        response = requests.request("PUT", url, json=payload, headers=headers)
        assert response.status_code == 200
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True

    def call_for_delete_faculty(self):
        title = FacultyOperationName.DELETE_FACULTY
        url = f"http://localhost:8000/v1/api/faculty/{self.update_instance_id}/"
        payload = ""
        headers = {"Authorization": f"Token {self.token}"}

        response = requests.request("DELETE", url, data=payload, headers=headers)
        assert response.status_code == 204
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True


class CourseRequestCall(GenerateRequestCallMixin):
    SET_OF_REQUEST_VALUES = {
        CourseOperationName.FETCH_COURSES: {},
        CourseOperationName.CREATE_COURSE: {},
        CourseOperationName.UPDATE_COURSE: {},
        CourseOperationName.DELETE_COURSE: {},
    }

    def run_and_collect(self):
        self.call_for_fetch_courses()
        self.call_for_create_course()
        self.call_for_update_course()
        self.call_for_delete_course()

    def call_for_fetch_courses(self):
        title = CourseOperationName.FETCH_COURSES
        url = "http://localhost:8000/v1/api/course/"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.request("GET", url, headers=headers)
        assert response.status_code == 200

        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_course(self):
        title = CourseOperationName.CREATE_COURSE
        url = "http://localhost:8000/v1/api/course/"
        payload = {
            "name": "Web Technology",
            "course_kind": "laboratory",
            "ects_for_course": 1,
            "faculty": Faculty.objects.last().id,
            "lecturer": Lecturer.objects.last().id,
            "grades": [],
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.token}",
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        assert response.status_code == 201
        self.update_instance_id = response.json().get("id")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True

    def call_for_update_course(self):
        title = CourseOperationName.UPDATE_COURSE
        url = f"http://localhost:8000/v1/api/course/{self.update_instance_id}/"
        payload = {
            "name": "Web Technology 4",
            "course_kind": "lecture",
            "ects_for_course": 2,
            "faculty": Faculty.objects.first().id,
            "lecturer": Lecturer.objects.first().id,
            "grades": [],
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.token}",
        }
        response = requests.request("PUT", url, json=payload, headers=headers)
        assert response.status_code == 200
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True

    def call_for_delete_course(self):
        title = CourseOperationName.DELETE_COURSE
        url = f"http://localhost:8000/v1/api/course/{self.update_instance_id}"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.request("DELETE", url, headers=headers)
        assert response.status_code == 204
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True
