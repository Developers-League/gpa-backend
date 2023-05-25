from base import calculate_fgpa
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from main import app
from model import Cgpa, Fgpa


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


def test_home_route(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"msg": "Welcome to the GPA app"}


def test_calculate_fgpa_endpoint(client):
    test_data = Fgpa(cgpa1=3.5, cgpa2=3.7, cgpa3=3.6, cgpa4=3.8)
    response = client.post("/api/calculate-fgpa", json=test_data.dict())
    expected_result = calculate_fgpa(test_data)

    assert response.status_code == 200
    assert response.json() == expected_result


def test_calculate_fgpa_invalid_data(client):
    invalid_data = {"cgpa1": -1.0, "cgpa2": 3.7, "cgpa3": 3.6, "cgpa4": 3.8}
    response = client.post("/api/calculate-fgpa", json=invalid_data)

    assert response.status_code == 400


def test_calculate_fgpa_missing_field(client):
    missing_field_data = {"cgpa1": 3.5, "cgpa2": 3.7, "cgpa3": 3.6}
    response = client.post("/api/calculate-fgpa", json=missing_field_data)

    assert response.status_code == 422


def test_calculate_min_max_cgpa_valid_data(client):
    valid_data = {"oldCgpa": 3.5, "oldChours": 90, "newChours": 30}

    response = client.post("/api/calc-min-max-gpa-per-sem", json=valid_data)
    expected_keys = [
        "oldCgpa",
        "maxCgpa",
        "minCgpa",
        "classificationMaxCgpa",
        "classificationMinCgpa",
    ]

    assert response.status_code == 200
    assert all(key in response.json() for key in expected_keys)


def test_calculate_min_max_cgpa_invalid_data(client):
    invalid_data = {"oldCgpa": 3.5, "oldChours": -10, "newChours": 30}
    response = client.post("/api/calc-min-max-gpa-per-sem", json=invalid_data)

    assert response.status_code == 400
    assert {
        "detail": "Negative values are not allowed for credit hours or CGPA."
    } == response.json()


def test_calc_new_gpa_valid_data(client):
    valid_data = {"grades": ["A", "B", "C"], "credit": [3, 4, 3]}
    response = client.post("/api/calc-gpa-and-cgpa", json=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()


def test_calc_new_gpa_invalid_grades(client):
    invalid_data = {"grades": ["A", "B", "X"], "credit": [3, 4, 3]}
    response = client.post("/api/calc-gpa-and-cgpa", json=invalid_data)

    assert response.status_code == 400


def test_calc_new_gpa_credit_hours_mismatch(client):
    invalid_data = {"grades": ["A", "B", "C"], "credit": [3, 4]}
    response = client.post("/api/calc-gpa-and-cgpa", json=invalid_data)

    assert response.status_code == 400


def test_calc_req_grades_valid_data(client):
    valid_data = {
        "oldCgpa": 3.5,
        "oldChours": 90,
        "newCgpa": 3.8,
        "newChours": 30,
        "courseNum": 6,
    }
    response = client.post("/api/calc-req-grades", json=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()


def test_calc_req_grades_high_cgpa(client):
    invalid_data = {
        "oldCgpa": 3.7,
        "oldChours": 90,
        "newCgpa": 4.5,
        "newChours": 30,
        "courseNum": 6,
    }
    response = client.post("/api/calc-req-grades", json=invalid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "Too high" in response.json()["feedback"]


def test_calc_req_grades_low_cgpa(client):
    invalid_data = {
        "oldCgpa": 3.7,
        "oldChours": 90,
        "newCgpa": -1.5,
        "newChours": 30,
        "courseNum": 6,
    }
    response = client.post("/api/calc-req-grades", json=invalid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "Too low" in response.json()["feedback"]


def test_calc_req_grades_fail_all_courses(client):
    invalid_data = {
        "oldCgpa": 3.0,
        "oldChours": 90,
        "newCgpa": 2.5,
        "newChours": 30,
        "courseNum": 6,
    }
    response = client.post("/api/calc-req-grades", json=invalid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()


def test_calc_req_grades_valid_req_grades(client):
    valid_data = {
        "oldCgpa": 3.5,
        "oldChours": 90,
        "newCgpa": 3.8,
        "newChours": 30,
        "courseNum": 6,
    }
    response = client.post("/api/calc-req-grades", json=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "Too high" in response.json()["feedback"]


def test_convert_weight_cgpa_to_cwa_valid(client):
    valid_data = {"cgpa": 3.5}
    response = client.get("/api/convert_weight", params=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "converted CGPA" in response.json()["feedback"]


def test_convert_weight_cwa_to_cgpa_valid(client):
    valid_data = {"cwa": 75}
    response = client.get("/api/convert_weight", params=valid_data)

    assert response.status_code == 200
    assert "feedback" in response.json()
    assert "converted CWA" in response.json()["feedback"]


def test_convert_weight_both_values_provided(client):
    invalid_data = {"cgpa": 3.5, "cwa": 70}
    response = client.get("/api/convert_weight", params=invalid_data)

    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Only one conversion value" in response.json()["detail"]


def test_convert_weight_invalid_cgpa_value(client):
    invalid_data = {"cgpa": 5.0}
    response = client.get("/api/convert_weight", params=invalid_data)

    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Invalid CGPA value" in response.json()["detail"]


def test_convert_weight_invalid_cwa_value(client):
    invalid_data = {"cwa": -10}
    response = client.get("/api/convert_weight", params=invalid_data)

    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Invalid CWA value" in response.json()["detail"]


def test_convert_weight_no_value_provided(client):
    response = client.get("/api/convert_weight")
    
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "No conversion value provided" in response.json()["detail"]
