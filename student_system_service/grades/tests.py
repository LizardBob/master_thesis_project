import json

import pytest
from django.urls import reverse
from rest_framework import status

from ..conftest import *  # noqa


@pytest.mark.django_db
def test_grade_model_create(simple_grades, simple_student, simple_lecturer):
    for simple_grade in simple_grades:
        assert simple_grade.value == GradeValue.AVERAGE
        assert not simple_grade.is_final_grade
        assert simple_grade.obtained_by == simple_student
        assert simple_grade.provided_by == simple_lecturer


@pytest.mark.django_db
def test_get_grades_list_view(api_client, simple_grades):
    url = reverse("api:grade-list")
    response = api_client.get(url)
    res_json = response.json().get("results")
    assert response.status_code == status.HTTP_200_OK
    assert len(res_json) == Grade.objects.count()

    all_grades = Grade.objects.all()

    for grade in res_json:
        expected_grade = all_grades.get(id=grade.get("id"))
        assert grade.get("id") == expected_grade.id
        assert grade.get("value") == expected_grade.value
        assert grade.get("is_final_grade") == expected_grade.is_final_grade
        assert grade.get("obtained_by") == expected_grade.obtained_by_id
        assert grade.get("provided_by") == expected_grade.provided_by_id


@pytest.mark.django_db
def test_create_grade_view(api_client, simple_grades, simple_lecturer, simple_student):
    url = reverse("api:grade-list")
    data = {
        "value": "D",
        "is_final_grade": False,
        "obtained_by": simple_student.id,
        "provided_by": simple_lecturer.id,
    }
    response = api_client.post(
        url, data=json.dumps(data), content_type="application/json"
    )
    res_json = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    new_grade = Grade.objects.last()

    assert res_json.get("id") == new_grade.id
    assert new_grade.value == res_json.get("value")
    assert new_grade.is_final_grade == res_json.get("is_final_grade")
    assert new_grade.obtained_by_id == res_json.get("obtained_by")
    assert new_grade.provided_by_id == res_json.get("provided_by")


@pytest.mark.django_db
def test_update_grade_view(
    api_client, simple_grades, simple_lecturers, simple_students
):
    updating_grade = simple_grades[0]
    url = reverse("api:grade-detail", args=[updating_grade.id])
    data = {
        "value": "A",
        "is_final_grade": True,
        "obtained_by": simple_students[-1].id,
        "provided_by": simple_lecturers[-1].id,
    }

    assert updating_grade.value != data.get("value")
    assert updating_grade.is_final_grade != data.get("is_final_grade")
    assert updating_grade.obtained_by_id != data.get("obtained_by")
    assert updating_grade.provided_by_id != data.get("provided_by")

    response = api_client.put(
        url, data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()

    updating_grade.refresh_from_db()

    assert updating_grade.value == res_json.get("value")
    assert updating_grade.is_final_grade == res_json.get("is_final_grade")
    assert updating_grade.obtained_by_id == res_json.get("obtained_by")
    assert updating_grade.provided_by_id == res_json.get("provided_by")


@pytest.mark.django_db
def test_delete_grade_view(api_client, simple_grades):
    deleting_grade = simple_grades[-1]
    url = reverse("api:grade-detail", args=[deleting_grade.id])
    response = api_client.delete(url, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
