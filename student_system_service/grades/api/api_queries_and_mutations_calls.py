import json

import faker
import requests

from student_system_service.core.const import GradeOperationName
from student_system_service.students.models import Student
from student_system_service.users.models import Lecturer

fake = faker.Faker()


class GradeQueryAndMutation:
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
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"query allGrades {\\n  allGrades (page:1) {\\n    page\\n    pages\\n    hasNext\\n    hasPrev\\n    objects{\\n      obtainedBy {\\n      id\\n    }\\n    providedBy {\\n      id\\n    }\\n    value\\n    isFinalGrade\\n    id\\n    }\\n  }\\n}","operationName":"allGrades"}'  # noqa
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_grade(self):
        title = GradeOperationName.CREATE_GRADE
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation createGrade($creaGra: GradeInput!) {\\n  createGrade(inputData: $creaGra) {\\n    grade{\\n      id\\n      value\\n      isFinalGrade\\n      obtainedBy{\\n        id\\n        name\\n        username\\n      }\\n      providedBy {\\n        id\\n        name\\n        username\\n      }\\n    }\\n  } \\n}","variables":{"creaGra":{"value":"B","isFinalGrade":false,"obtainedBy":24050,"providedBy":24052}},"operationName":"createGrade"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables").get("creaGra")[
            "providedBy"
        ] = Lecturer.objects.last().id
        payload.get("variables").get("creaGra")[
            "obtainedBy"
        ] = Student.objects.last().id
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.update_instance_id = (
            response.json().get("data").get("createGrade").get("grade").get("id")
        )
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_update_grade(self):
        title = GradeOperationName.UPDATE_GRADE
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation updateGrade($updGra: GradeInput) {\\n  updateGrade(inputData: $updGra) {\\n    grade{\\n      id\\n      value\\n      isFinalGrade\\n      obtainedBy{\\n        id\\n        name\\n        username\\n      }\\n      providedBy {\\n        id\\n        name\\n        username\\n      }\\n    }\\n  }\\n}","variables":{"updGra":{"id":21,"value":"B","isFinalGrade":false,"obtainedBy":4,"providedBy":1}},"operationName":"updateGrade"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables").get("updGra")["id"] = self.update_instance_id
        payload.get("variables").get("updGra")[
            "providedBy"
        ] = Lecturer.objects.first().id
        payload.get("variables").get("updGra")[
            "obtainedBy"
        ] = Student.objects.first().id
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_delete_grade(self):
        title = GradeOperationName.DELETE_GRADE
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation deleteGrade($delGra: Int) {\\n  deleteGrade(id: $delGra) {\\n    ok\\n  }\\n}","variables":{"delGra":21},"operationName":"deleteGrade"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables")["delGra"] = self.update_instance_id
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True
