import faker
import requests

from student_system_service.core.const import (
    GenerateRequestCallMixin,
    GradeOperationName,
)
from student_system_service.students.models import Student
from student_system_service.users.models import Lecturer

fake = faker.Faker()


class GradeRequestCall(GenerateRequestCallMixin):
    SET_OF_REQUEST_VALUES = {
        GradeOperationName.FETCH_GRADES: {},
        GradeOperationName.CREATE_GRADE: {},
        GradeOperationName.UPDATE_GRADE: {},
        GradeOperationName.DELETE_GRADE: {},
    }

    def run_and_collect(self):
        self.call_for_fetch_grades()
        self.call_for_create_grade()
        self.call_for_update_grade()
        self.call_for_delete_grade()

    def call_for_fetch_grades(self):
        title = GradeOperationName.FETCH_GRADES
        url = "http://localhost:8000/v1/api/grade/"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.request("GET", url, headers=headers)
        assert response.status_code == 200
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_grade(self):
        title = GradeOperationName.CREATE_GRADE
        url = "http://localhost:8000/v1/api/grade/"
        payload = {
            "value": "A",
            "is_final_grade": True,
            "obtained_by": Student.objects.last().id,
            "provided_by": Lecturer.objects.last().id,
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

    def call_for_update_grade(self):
        title = GradeOperationName.UPDATE_GRADE
        url = f"http://localhost:8000/v1/api/grade/{self.update_instance_id}/"

        payload = {
            "value": "B",
            "is_final_grade": False,
            "obtained_by": Student.objects.first().id,
            "provided_by": Lecturer.objects.first().id,
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

    def call_for_delete_grade(self):
        title = GradeOperationName.DELETE_GRADE
        url = f"http://localhost:8000/v1/api/grade/{self.update_instance_id}/"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.request("DELETE", url, headers=headers)
        assert response.status_code == 204
        self.SET_OF_REQUEST_VALUES[title].update(
            {"REST": response.elapsed.total_seconds()}
        )
        return True
