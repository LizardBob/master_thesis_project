import faker
import requests

from student_system_service.core.const import (
    GenerateRequestCallMixin,
    StudentOperationName,
)
from student_system_service.courses.models import Faculty

fake = faker.Faker()


class StudentRequestCall(GenerateRequestCallMixin):
    SET_OF_REQUEST_VALUES = {
        StudentOperationName.FETCH_STUDENTS: {},
        StudentOperationName.CREATE_STUDENT: {},
        StudentOperationName.UPDATE_STUDENT: {},
        StudentOperationName.DELETE_STUDENT: {},
    }

    def run_and_collect(self):
        self.call_for_fetch_students()
        self.call_for_create_student()
        self.call_for_update_student()
        self.call_for_delete_student()

    def call_for_fetch_students(self):
        title = StudentOperationName.FETCH_STUDENTS
        url = "http://localhost:8000/v1/api/students/"

        headers = {"Authorization": f"Token {self.token}"}

        response = requests.request("GET", url, headers=headers)
        assert response.status_code == 200
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_student(self):
        title = StudentOperationName.CREATE_STUDENT
        url = "http://localhost:8000/v1/api/students/"

        payload = {
            "password": "123",
            "username": f"{fake.isbn10()}",
            "email": "a2a@example.com",
            "name": "a2name",
            "faculty": Faculty.objects.last().id,
            "courses": [],
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

    def call_for_update_student(self):
        title = StudentOperationName.UPDATE_STUDENT
        url = f"http://localhost:8000/v1/api/students/{self.update_instance_id}/"

        payload = {
            "password": "321",
            "username": f"{fake.isbn10()}",
            "email": "A1A@example.com",
            "name": "A1nAme",
            "faculty": Faculty.objects.first().id,
            "courses": [],
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

    def call_for_delete_student(self):
        title = StudentOperationName.DELETE_STUDENT
        url = f"http://localhost:8000/v1/api/students/{self.update_instance_id}"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.request("DELETE", url, headers=headers)
        assert response.status_code == 204
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True
