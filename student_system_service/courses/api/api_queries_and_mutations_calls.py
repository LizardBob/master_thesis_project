import json

import faker
import requests

from student_system_service.core.const import CourseOperationName, FacultyOperationName
from student_system_service.courses.models import Faculty
from student_system_service.users.models import Lecturer

fake = faker.Faker()


class FacultyQueryAndMutation:
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
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"query allFaculties {\\n  allFaculties(page: 1) {\\n    page\\n    pages\\n    hasNext\\n    hasPrev\\n    objects {\\n      id\\n      name\\n#       students {\\n#         id\\n#         indexCode\\n#       }\\n    }\\n  }\\n}\\n","operationName":"allFaculties"}'  # noqa
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_faculty(self):
        title = FacultyOperationName.CREATE_FACULTY
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation createFaculty($crefa: FacultyInput!) {\\n  createFaculty(inputData: $crefa) {\\n    faculty{\\n      id\\n      name\\n    }\\n  }\\n}","variables":{"crefa":{"name":"Faculty Of Information and Technology"}},"operationName":"createFaculty"}'  # noqa
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.updating_instance_id = (
            response.json().get("data").get("createFaculty").get("faculty").get("id")
        )
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_update_faculty(self):
        title = FacultyOperationName.UPDATE_FACULTY
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation updateFaculty($updfa: FacultyUpdateMutationInput!) {\\n  updateFaculty(input: $updfa) {\\n    id\\n    name\\n  }\\n}","variables":{"updfa":{"id":5,"name":"Faculty of Electronics"}},"operationName":"updateFaculty"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables").get("updfa")["id"] = self.updating_instance_id
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

    def call_for_delete_faculty(self):
        title = FacultyOperationName.DELETE_FACULTY
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation deleteFaculty($dfa: Int) {\\n  deleteFaculty(id: $dfa) {\\n    ok\\n  }\\n}\\n","variables":{"dfa":6},"operationName":"deleteFaculty"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables")["dfa"] = self.updating_instance_id
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


class CourseQueryAndMutation:
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
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"query allCourses {\\n  allCourses(page: 1) {\\n    page\\n    pages\\n    hasNext\\n    hasPrev\\n    objects {\\n      id\\n      name\\n      courseCode\\n      courseKind\\n      ectsForCourse\\n      faculty {\\n        id\\n      }\\n      grades\\n      lecturer {\\n        id\\n      }\\n    }\\n  }\\n}\\n","operationName":"allCourses"}'  # noqa
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_create_course(self):
        title = CourseOperationName.CREATE_COURSE
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation createCourse($creCourse: CourseInput!) {\\n  createCourse(inputData: $creCourse) {\\n    course {\\n      id\\n      name\\n      courseCode\\n      courseKind\\n      ectsForCourse\\n      faculty {\\n        id\\n      }\\n      lecturer {\\n        id\\n      }\\n      grades\\n    }\\n  }\\n}","variables":{"creCourse":{"name":"New Course Programming","courseKind":"laboratory","ectsForCourse":2,"faculty":1,"lecturer":1,"grades":[]}},"operationName":"createCourse"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables").get("creCourse")["faculty"] = Faculty.objects.last().id
        payload.get("variables").get("creCourse")[
            "lecturer"
        ] = Lecturer.objects.last().id
        payload = json.dumps(payload)
        headers = {
            "cookie": "csrftoken=wIfF4QGqdXTH4rzh6DU3U66Q5wwObAXebIHXEwGz9pCMArwXE46d1yMC8rBams5g",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.update_instance_id = (
            response.json().get("data").get("createCourse").get("course").get("id")
        )
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_update_course(self):
        title = CourseOperationName.UPDATE_COURSE
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation updateCourse($updCpurse: CourseInput!) {\\n  updateCourse(inputData: $updCpurse) {\\n    course {\\n      id\\n      name\\n      courseCode\\n      courseKind\\n      ectsForCourse\\n      faculty {\\n        id\\n      }\\n      lecturer {\\n        id\\n      }\\n      grades\\n    }\\n  }\\n}","variables":{"updCpurse":{"id":10,"name":"Advanced Course Programming","courseKind":"laboratory","ectsForCourse":2,"faculty":1,"lecturer":1,"grades":[1]}},"operationName":"updateCourse"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables").get("updCpurse")["id"] = self.update_instance_id
        payload.get("variables").get("updCpurse")[
            "faculty"
        ] = Faculty.objects.first().id
        payload.get("variables").get("updCpurse")[
            "lecturer"
        ] = Lecturer.objects.first().id
        payload.get("variables").get("updCpurse")["grades"] = []
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True

    def call_for_delete_course(self):
        title = CourseOperationName.DELETE_COURSE
        url = "http://localhost:8000/graphql/"
        payload = '{"query":"mutation deleteCourse($deleCour: Int) {\\n  deleteCourse(id: $deleCour) {\\n    ok\\n  }\\n}","variables":{"deleCour":10},"operationName":"deleteCourse"}'  # noqa
        payload = json.loads(payload)
        payload.get("variables")["deleCour"] = self.update_instance_id
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        assert response.status_code == 200
        assert "errors" not in response.content.decode("utf8")
        self.SET_OF_REQUEST_VALUES[title].update(
            {"GraphQL API": response.elapsed.total_seconds()}
        )
        return True
