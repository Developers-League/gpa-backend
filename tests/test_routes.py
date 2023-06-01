import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.main import app
from src.models.model import Fgpa
from src.services.gpa import calculate_fgpa


@pytest.fixture(scope="module")
def client() -> FastAPI:
    with TestClient(app) as client:
        yield client


def test_home_route(client: FastAPI):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"msg": "Welcome to the GPA app"}


def test_calculate_fgpa_endpoint(client: FastAPI):
    test_data = Fgpa(cgpa1=3.5, cgpa2=3.7, cgpa3=3.6, cgpa4=3.8)
    response = client.post("/api/calculate-fgpa", json=test_data.dict())
    expected_result = calculate_fgpa(test_data)

    assert response.status_code == 200
    assert response.json() == expected_result


def test_calculate_fgpa_invalid_data(client: FastAPI):
    invalid_data = {"cgpa1": -1.0, "cgpa2": 3.7, "cgpa3": 3.6, "cgpa4": 3.8}
    response = client.post("/api/calculate-fgpa", json=invalid_data)

    assert response.status_code == 400


def test_calculate_fgpa_missing_field(client: FastAPI):
    missing_field_data = {"cgpa1": 3.5, "cgpa2": 3.7, "cgpa3": 3.6}
    response = client.post("/api/calculate-fgpa", json=missing_field_data)

    assert response.status_code == 422


def test_calculate_min_max_cgpa_valid_data(client: FastAPI):
    valid_data = {"old_cgpa": 3.5, "old_chours": 90, "new_chours": 30}

    response = client.post("/api/calc-min-max-gpa-per-sem", json=valid_data)
    expected_keys = [
        "old_cgpa",
        "max_cgpa",
        "min_cgpa",
        "classification_max_cgpa",
        "classification_min_cgpa",
    ]

    assert response.status_code == 200
    assert all(key in response.json() for key in expected_keys)


def test_calculate_min_max_cgpa_invalid_data(client: FastAPI):
    invalid_data = {"old_cgpa": 3.5, "old_chours": -10, "new_chours": 30}
    response = client.post("/api/calc-min-max-gpa-per-sem", json=invalid_data)

    assert response.status_code == 400
    assert {
        "detail": "Negative values are not allowed for credit hours or CGPA."
    } == response.json()


def test_calc_new_gpa_valid_data(client: FastAPI):
    valid_data = {"grades": ["A", "B", "C"], "credit": [3, 4, 3]}
    response = client.post("/api/calc-gpa-and-cgpa", json=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()


def test_calc_new_gpa_invalid_grades(client: FastAPI):
    invalid_data = {"grades": ["A", "B", "X"], "credit": [3, 4, 3]}
    response = client.post("/api/calc-gpa-and-cgpa", json=invalid_data)

    assert response.status_code == 400


def test_calc_new_gpa_credit_hours_mismatch(client: FastAPI):
    invalid_data = {"grades": ["A", "B", "C"], "credit": [3, 4]}
    response = client.post("/api/calc-gpa-and-cgpa", json=invalid_data)

    assert response.status_code == 400


def test_calc_req_grades_valid_data(client: FastAPI):
    valid_data = {
        "old_cgpa": 3.5,
        "old_chours": 90,
        "new_cgpa": 3.8,
        "new_chours": 30,
        "course_num": 6,
    }
    response = client.post("/api/calc-req-grades", json=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()


def test_calc_req_grades_high_cgpa(client: FastAPI):
    invalid_data = {
        "old_cgpa": 3.7,
        "old_chours": 90,
        "new_cgpa": 4.5,
        "new_chours": 30,
        "course_num": 6,
    }
    response = client.post("/api/calc-req-grades", json=invalid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "Too high" in response.json()["feedback"]


def test_calc_req_grades_low_cgpa(client: FastAPI):
    invalid_data = {
        "old_cgpa": 3.7,
        "old_chours": 90,
        "new_cgpa": -1.5,
        "new_chours": 30,
        "course_num": 6,
    }
    response = client.post("/api/calc-req-grades", json=invalid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "Too low" in response.json()["feedback"]


def test_calc_req_grades_fail_all_courses(client: FastAPI):
    invalid_data = {
        "old_cgpa": 3.0,
        "old_chours": 90,
        "new_cgpa": 2.5,
        "new_chours": 30,
        "course_num": 6,
    }
    response = client.post("/api/calc-req-grades", json=invalid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()


def test_calc_req_grades_valid_req_grades(client: FastAPI):
    valid_data = {
        "old_cgpa": 3.5,
        "old_chours": 90,
        "new_cgpa": 3.8,
        "new_chours": 30,
        "course_num": 6,
    }
    response = client.post("/api/calc-req-grades", json=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "Too high" in response.json()["feedback"]


def test_convert_weight_cgpa_to_cwa_valid(client: FastAPI):
    valid_data = {"cgpa": 3.5}
    response = client.get("/api/convert_weight", params=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "converted CGPA" in response.json()["feedback"]


def test_convert_weight_cwa_to_cgpa_valid(client: FastAPI):
    valid_data = {"cwa": 75}
    response = client.get("/api/convert_weight", params=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "converted CWA" in response.json()["feedback"]


def test_convert_weight_both_values_provided(client: FastAPI):
    invalid_data = {"cgpa": 3.5, "cwa": 70}
    response = client.get("/api/convert_weight", params=invalid_data)

    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Only one conversion value" in response.json()["detail"]


def test_convert_weight_invalid_cgpa_value(client: FastAPI):
    invalid_data = {"cgpa": 5.0}
    response = client.get("/api/convert_weight", params=invalid_data)

    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Invalid CGPA value" in response.json()["detail"]


def test_convert_weight_invalid_cwa_value(client: FastAPI):
    invalid_data = {"cwa": -10}
    response = client.get("/api/convert_weight", params=invalid_data)

    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Invalid CWA value" in response.json()["detail"]


def test_convert_weight_no_value_provided(client: FastAPI):
    response = client.get("/api/convert_weight")

    assert response.status_code == 400
    assert "detail" in response.json()
    assert "No conversion value provided" in response.json()["detail"]
