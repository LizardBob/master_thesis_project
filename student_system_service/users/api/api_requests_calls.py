import faker
import requests

from student_system_service.core.const import (
    GenerateRequestCallMixin,
    LecturerOperationName,
)

fake = faker.Faker()


class LecturerRequestCall(GenerateRequestCallMixin):
    SET_OF_REQUEST_VALUES = {
        LecturerOperationName.FETCH_LECTURERS: {},
        LecturerOperationName.CREATE_LECTURER: {},
        LecturerOperationName.UPDATE_LECTURER: {},
        LecturerOperationName.DELETE_LECTURER: {},
    }

    def run_and_collect(self):
        self.call_for_fetch_lecturer()
        self.call_for_create_lecturer()
        self.call_for_update_lecturer()
        self.call_for_delete_lecturer()

    def call_for_fetch_lecturer(self):
        title = LecturerOperationName.FETCH_LECTURERS
        url = "http://localhost:8000/v1/api/lecturer/"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.request("GET", url, headers=headers)
        assert response.status_code == 200

        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_lecturer(self):
        title = LecturerOperationName.CREATE_LECTURER
        url = "http://localhost:8000/v1/api/lecturer/"

        payload = {
            "password": "123",
            "username": f"{fake.isbn10()}",
            "email": "lec1@example.com",
            "name": "Lec1",
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

    def call_for_update_lecturer(self):
        title = LecturerOperationName.UPDATE_LECTURER
        url = f"http://localhost:8000/v1/api/lecturer/{self.update_instance_id}/"
        payload = {
            "password": "321",
            "username": f"{fake.isbn10()}",
            "email": "lec2@example.com",
            "name": "Lec2",
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

    def call_for_delete_lecturer(self):
        title = LecturerOperationName.DELETE_LECTURER
        url = f"http://localhost:8000/v1/api/lecturer/{self.update_instance_id}/"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.request("DELETE", url, headers=headers)
        assert response.status_code == 204
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True
