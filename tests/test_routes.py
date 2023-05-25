from typing import NamedTuple
from base import calculate_fgpa
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from main import app
from model import Fgpa


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
