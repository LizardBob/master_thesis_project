import json

import faker
import requests

from student_system_service.core.const import StudentOperationName
from student_system_service.courses.models import Faculty

fake = faker.Faker()


class StudentQueryAndMutation:
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
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"query allStudentsQuery {\\n  allStudents(page: 1) {\\n    page\\n    pages\\n    hasNext\\n    hasPrev\\n    objects{\\n      id\\n    name\\n    username\\n    email\\n    indexCode\\n    faculty {\\n      id\\n      name\\n    }\\n    courses {\\n      id\\n      name\\n      courseCode\\n      courseKind\\n      ectsForCourse\\n#       faculty {\\n#         id\\n#         name\\n#       }\\n#       grades {\\n#         value\\n#         isFinalGrade\\n#         obtainedBy {\\n#           id\\n#           name\\n#         }\\n#       }\\n    }\\n    }\\n    \\n  }\\n}","operationName":"allStudentsQuery"}'  # noqa
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_student(self):
        title = StudentOperationName.CREATE_STUDENT
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation createStudent($createStudentPayload: StudentInput!) {\\n  createStudent(inputData: $createStudentPayload) {\\n    student {\\n      id\\n      username\\n      email\\n      faculty {\\n        id\\n      }\\n      name\\n    }\\n  }\\n}","variables":{"createStudentPayload":{"password":"123","username":"LOL-1studentQL","email":"gql@test.com","name":"GTest","faculty":1}},"operationName":"createStudent"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables").get("createStudentPayload")[
            "faculty"
        ] = Faculty.objects.last().id
        payload.get("variables").get("createStudentPayload")[
            "username"
        ] = f"{fake.isbn10()}"
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.updating_instance_id = (
            response.json().get("data").get("createStudent").get("student").get("id")
        )
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_update_student(self):
        title = StudentOperationName.UPDATE_STUDENT
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation updateStudent($updateStudentPayload: StudentUpdateMutationInput!) {\\n  updateStudent(input: $updateStudentPayload) {\\n    id\\n    username\\n    email\\n    faculty\\n    name\\n  }\\n}","variables":{"updateStudentPayload":{"id":7,"password":"123","username":"G_1studentQL","email":"g1q1l@test.com","name":"GTe23st","faculty":"1"}},"operationName":"updateStudent"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables").get("updateStudentPayload")[
            "faculty"
        ] = Faculty.objects.first().id
        payload.get("variables").get("updateStudentPayload")[
            "id"
        ] = self.updating_instance_id
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_delete_student(self):
        title = StudentOperationName.DELETE_STUDENT
        url = "http://localhost:8000/graphql/"

        payload = '{"query":"mutation deleteStudent($deleteStudentPayload: Int) {\\n  deleteStudent(id: $deleteStudentPayload) {\\n    ok\\n  }\\n}\\n","variables":{"deleteStudentPayload":7},"operationName":"deleteStudent"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables")["deleteStudentPayload"] = self.updating_instance_id
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True
