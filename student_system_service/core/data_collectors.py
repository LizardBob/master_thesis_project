import json
import os
import sys

import environ

from student_system_service.courses.api.api_requests_calls import (
    CourseRequestCall,
    FacultyRequestCall,
)
from student_system_service.grades.api.api_requests_calls import GradeRequestCall
from student_system_service.students.api.api_requestes_calls import StudentRequestCall
from student_system_service.users.api.api_requests_calls import LecturerRequestCall

env = environ.Env()


class CollectRestApiData:
    REST_API_REQUEST_DATA = {}

    def __init__(self):
        self.student_requests = StudentRequestCall()
        self.faculty_requests = FacultyRequestCall()
        self.lecturer_requests = LecturerRequestCall()
        self.course_requests = CourseRequestCall()
        self.grade_requests = GradeRequestCall()
        self.collect()
        self.save_to_file_rest_requests_data()

    def collect(self):
        self.student_requests.run_and_collect()
        self.faculty_requests.run_and_collect()
        self.lecturer_requests.run_and_collect()
        self.course_requests.run_and_collect()
        self.grade_requests.run_and_collect()

    def save_to_file_rest_requests_data(self):
        self.REST_API_REQUEST_DATA.update(
            **self.student_requests.SET_OF_REQUEST_VALUES,
            **self.faculty_requests.SET_OF_REQUEST_VALUES,
            **self.lecturer_requests.SET_OF_REQUEST_VALUES,
            **self.course_requests.SET_OF_REQUEST_VALUES,
            **self.grade_requests.SET_OF_REQUEST_VALUES,
        )

        # print(self.REST_API_REQUEST_DATA)
        my_file = env("FILE_FOR_RESEARCHES_DATA")

        if os.path.getsize(my_file):
            self.show_quick_summary_after_opt_for_rest(my_file)
        try:
            convert_file = open(my_file, "w+")
            convert_file.write(json.dumps(self.REST_API_REQUEST_DATA))
        except Exception as e:
            sys.stdout.write(f"***** {e} ******")
        convert_file.close()

        sys.stdout.write(f"Collect and Store data\nCheck file here {my_file}\nFinished")

    def show_quick_summary_after_opt_for_rest(self, my_file):
        file_with_data_before_opt = open(my_file, "r+")
        old_object_values = json.loads(file_with_data_before_opt.readlines()[0])
        nice_icon = "\U0001F7E2"
        bad_icon = "\U0001F7E5"

        for key, values in old_object_values.items():
            if "Fetch" in key:
                prev_value = old_object_values.get(key).get("REST")
                new_value = self.REST_API_REQUEST_DATA.get(key).get("REST")

                if new_value < prev_value:

                    approve_message = (
                        f"We did improve about: {prev_value - new_value:.2f} seconds | "
                    )
                    sys.stdout.write(f"For {key} => {approve_message} {nice_icon}\n")
                else:
                    sys.stdout.write(f"For {key} => We did not approve | {bad_icon}\n")

        file_with_data_before_opt.close()
