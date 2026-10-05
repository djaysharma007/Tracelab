from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_api_list_algorithms():
    response = client.get("/api/algorithms")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 28


def test_api_generate_preset():
    response = client.post("/api/generate", json={"algorithm_id": "bubble_sort", "preset_name": "normal"})
    assert response.status_code == 200
    data = response.json()
    assert "input" in data
    assert "array" in data["input"]


def test_api_run_success():
    response = client.post("/api/run", json={"algorithm_id": "bubble_sort", "input": {"array": [5, 2, 8, 1]}})
    assert response.status_code == 200
    data = response.json()
    assert data["algorithm_id"] == "bubble_sort"
    assert data["total_steps"] > 0
    assert "metrics" in data


def test_api_run_validation_error():
    response = client.post("/api/run", json={"algorithm_id": "bubble_sort", "input": {"array": []}})
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_api_compare():
    payload = {
        "group": "Sorting",
        "algorithm_ids": ["bubble_sort", "quick_sort"],
        "input_kind": "random",
        "sizes": [10, 20],
        "repeats": 2,
        "seed": 42
    }
    response = client.post("/api/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "series" in data
    assert "bubble_sort" in data["series"]
    assert "quick_sort" in data["series"]
