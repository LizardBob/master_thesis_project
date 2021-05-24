import json

import faker
import requests

from student_system_service.core.const import LecturerOperationName

fake = faker.Faker()


class LecturerQueryAndMutation:
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
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"query allLecturers {\\n  allLecturers (page: 1) {\\n    page\\n    pages\\n    hasNext\\n    hasPrev\\n    objects{\\n      id\\n    indexCode\\n    email\\n    username\\n    name\\n    courses\\n    }\\n  }\\n}","operationName":"allLecturers"}'  # noqa
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_lecturer(self):
        title = LecturerOperationName.CREATE_LECTURER
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation createLecturer($LecturerData: LecturerInput!) {\\n  createLecturer(inputData: $LecturerData) {\\n    lecturer {\\n      id\\n      indexCode\\n      name\\n      username\\n      courses\\n    }\\n  }\\n}","variables":{"LecturerData":{"password":"123","username":"Lec321t_1Test","email":"lec1Test@test.com","name":"K Drapa"}},"operationName":"createLecturer"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables").get("LecturerData")["username"] = f"{fake.isbn10()}"
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.update_instance_id = (
            response.json().get("data").get("createLecturer").get("lecturer").get("id")
        )
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_update_lecturer(self):
        title = LecturerOperationName.UPDATE_LECTURER
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation updateLecturer($luD: LecturerUpdateMutationInput!) {\\n  updateLecturer(input: $luD) {\\n    id\\n    password\\n    email\\n    username\\n    name\\n    courses \\n  }\\n}","variables":{"luD":{"id":8,"password":"432","username":"TestL4ec","email":"TestLec@test.com","name":"DrapaK"}},"operationName":"updateLecturer"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables").get("luD")["id"] = self.update_instance_id
        payload.get("variables").get("luD")["username"] = f"{fake.isbn10()}"
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_delete_lecturer(self):
        title = LecturerOperationName.DELETE_LECTURER
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation deleteLecturer($dl: Int) {\\n  deleteLecturer(id: $dl) {\\n    ok\\n  }\\n}","variables":{"dl":8},"operationName":"deleteLecturer"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables")["dl"] = self.update_instance_id
        payload = json.dumps(payload)
        headers = {
            "cookie": "csrftoken=wIfF4QGqdXTH4rzh6DU3U66Q5wwObAXebIHXEwGz9pCMArwXE46d1yMC8rBams5g",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True
