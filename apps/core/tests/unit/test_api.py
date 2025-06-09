import pytest
import json
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api")


@pytest.mark.parametrize(
    "endpoint, payload, expected_status",
    [
        ("/questionlogs/", {"title": "New Question", "difficulty": "Easy"}, 201),
        ("/questionlogs/", {}, 400),
        ("/tags/", {"name": "New Tag"}, 201),
        ("/tags/", {}, 400),
    ],
)
def test_create_views(request_context, endpoint, payload, expected_status):
    # If testing questionlogs, ensure a question exists and add its ID to the payload
    if endpoint == "/questionlogs/" and expected_status == 201:
        # Create a question first with all required fields
        question_payload = {
            "title": "Test Question for Log",
            "slug": "test-question-for-log",
            "difficulty": "Easy"
        }
        question_response = request_context.post(f"{API_URL}/questions/", data=json.dumps(question_payload))
        assert question_response.status == 201
        question_id = question_response.json()["id"]
        payload = dict(payload)
        payload["question"] = question_id
    # If testing tags, ensure 'name' is present for 201
    if endpoint == "/tags/" and expected_status == 201 and "name" not in payload:
        payload = dict(payload)
        payload["name"] = "Auto Tag"
    response = request_context.post(f"{API_URL}{endpoint}", data=json.dumps(payload))
    assert response.status == expected_status


@pytest.mark.parametrize(
    "endpoint, method, expected_status",
    [
        ("/questionlogs/", "GET", 200),
        ("/tags/", "GET", 200),
    ],
)
def test_list_views(request_context, endpoint, method, expected_status):
    if method == "GET":
        response = request_context.get(f"{API_URL}{endpoint}")
    else:
        response = request_context.post(f"{API_URL}{endpoint}")
    assert response.status == expected_status


@pytest.mark.parametrize(
    "endpoint, payload, expected_status",
    [
        (
            "/questionlogs/1/",
            {"title": "Updated Question", "difficulty": "Medium"},
            200,
        ),
        ("/tags/1/", {"name": "Updated Tag"}, 200),
    ],
)
def test_update_views(request_context, endpoint, payload, expected_status):
    response = request_context.put(f"{API_URL}{endpoint}", data=json.dumps(payload))
    assert response.status == expected_status


@pytest.mark.parametrize(
    "endpoint, expected_status",
    [
        ("/questionlogs/1/", 204),
        ("/tags/1/", 204),
    ],
)
def test_delete_views(request_context, endpoint, expected_status):
    response = request_context.delete(f"{API_URL}{endpoint}")
    assert response.status == expected_status


@pytest.mark.parametrize(
    "endpoint, payload, expected_status",
    [
        ("/questions/", {"title": "FizzBuzz", "slug": "fizz-buzz"}, 201),
        ("/questions/", {}, 400),
        ("/questions/", {"title": "Only Title"}, 400),
        ("/questions/", {"slug": "only-slug"}, 400),
    ],
)
def test_create_question_api(request_context, endpoint, payload, expected_status):
    response = request_context.post(f"{API_URL}{endpoint}", data=json.dumps(payload))
    if response.status != expected_status:
        print("Response status:", response.status)
        print("Response body:", response.json())
    assert response.status == expected_status
