# import json
import sys

import environ

from student_system_service.courses.api.api_queries_and_mutations_calls import (
    CourseQueryAndMutation,
    FacultyQueryAndMutation,
)
from student_system_service.grades.api.api_queries_and_mutations_calls import (
    GradeQueryAndMutation,
)
from student_system_service.students.api.api_queries_and_mutations_calls import (
    StudentQueryAndMutation,
)
from student_system_service.users.api.api_queries_and_mutations_calls import (
    LecturerQueryAndMutation,
)

env = environ.Env()


class CollectGraphQLApiData:
    GRAPHQL_API_REQUEST_DATA = {}

    def __init__(self):
        self.student_requests = StudentQueryAndMutation()
        self.faculty_requests = FacultyQueryAndMutation()
        self.lecturer_requests = LecturerQueryAndMutation()
        self.course_requests = CourseQueryAndMutation()
        self.grade_requests = GradeQueryAndMutation()
        self.collect()

    def collect(self):
        self.student_requests.run_and_collect()
        self.faculty_requests.run_and_collect()
        self.lecturer_requests.run_and_collect()
        self.course_requests.run_and_collect()
        self.grade_requests.run_and_collect()

    def save_to_file_rest_requests_data(self):
        self.GRAPHQL_API_REQUEST_DATA.update(
            **self.student_requests.SET_OF_REQUEST_VALUES,
            **self.faculty_requests.SET_OF_REQUEST_VALUES,
            **self.lecturer_requests.SET_OF_REQUEST_VALUES,
            **self.course_requests.SET_OF_REQUEST_VALUES,
            **self.grade_requests.SET_OF_REQUEST_VALUES,
        )
        my_file = env("FILE_FOR_RESEARCHES_DATA")
        try:
            convert_file = open(my_file, "r+")
            rest_api_data = convert_file.readlines()
            print(rest_api_data, type(rest_api_data))
            # obj_with_rest_api_data = json.dumps()
            # convert_file.write(json.dumps(self.GRAPHQL_API_REQUEST_DATA))

        except Exception as e:
            sys.stdout.write(f"***** {e} ******")
        convert_file.close()

        sys.stdout.write(
            f"Collect and not yet Store data\nCheck file here {my_file}\nFinished"
        )
