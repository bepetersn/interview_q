import pytest
import json
from django.test import Client


@pytest.fixture(scope="module")
def client():
    return Client()


def _create_questionlog_and_dependencies(client):
    # Ensure a question exists for the foreign key
    question_payload = {"title": "Test Q", "slug": "test-q", "difficulty": "Easy"}
    client.post("/api/questions/", data=json.dumps(question_payload), content_type="application/json")
    create_payload = {"title": "Original Question", "difficulty": "Easy", "question": 1}
    client.post("/api/questionlogs/", data=json.dumps(create_payload), content_type="application/json")


def _create_tag(client):
    create_payload = {"name": "Original Tag"}
    client.post("/api/tags/", data=json.dumps(create_payload), content_type="application/json")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, payload, expected_status",
    [
        ("/api/questionlogs/", {"title": "New Question", "difficulty": "Easy"}, 201),
        ("/api/questionlogs/", {}, 400),
        ("/api/tags/", {"name": "New Tag"}, 201),
        ("/api/tags/", {}, 400),
    ],
)
def test_create_views(client, endpoint, payload, expected_status):
    # If testing questionlogs, ensure a question exists and add its ID to the payload
    if endpoint == "/api/questionlogs/" and expected_status == 201:
        question_payload = {
            "title": "Test Question for Log",
            "slug": "test-question-for-log",
            "difficulty": "Easy"
        }
        question_response = client.post("/api/questions/", data=json.dumps(question_payload), content_type="application/json")
        assert question_response.status_code == 201
        question_id = question_response.json()["id"]
        payload = dict(payload)
        payload["question"] = question_id
    # If testing tags, ensure 'name' is present for 201
    if endpoint == "/api/tags/" and expected_status == 201 and "name" not in payload:
        payload = dict(payload)
        payload["name"] = "Auto Tag"
    response = client.post(endpoint, data=json.dumps(payload), content_type="application/json")
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, method, expected_status",
    [
        ("/api/questionlogs/", "GET", 200),
        ("/api/tags/", "GET", 200),
    ],
)
def test_list_views(client, endpoint, method, expected_status):
    if method == "GET":
        response = client.get(endpoint)
    else:
        response = client.post(endpoint)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, payload, expected_status",
    [
        (
            "/api/questionlogs/1/",
            {"title": "Updated Question", "difficulty": "Medium"},
            200,
        ),
        ("/api/tags/1/", {"name": "Updated Tag"}, 200),
    ],
)
def test_update_views(client, endpoint, payload, expected_status):
    if endpoint.startswith("/api/questionlogs/"):
        _create_questionlog_and_dependencies(client)
    elif endpoint.startswith("/api/tags/"):
        _create_tag(client)
    response = client.put(endpoint, data=json.dumps(payload), content_type="application/json")
    if endpoint.startswith("/api/questionlogs/"):
        get_response = client.get(endpoint)
        assert get_response.status_code == 200
        data = get_response.json()
        # TODO: Not sure why, but not working as expected
        for key, value in payload.items():
            assert data[key] == value
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, expected_status",
    [
        ("/api/questionlogs/1/", 204),
        ("/api/tags/1/", 204),
    ],
)
def test_delete_views(client, endpoint, expected_status):
    if endpoint.startswith("/api/questionlogs/"):
        _create_questionlog_and_dependencies(client)
    elif endpoint.startswith("/api/tags/"):
        _create_tag(client)
    response = client.delete(endpoint)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, payload, expected_status",
    [
        ("/api/questions/", {"title": "FizzBuzz", "slug": "fizz-buzz"}, 201),
        ("/api/questions/", {}, 400),
        ("/api/questions/", {"title": "Only Title"}, 400),
        ("/api/questions/", {"slug": "only-slug"}, 400),
    ],
)
def test_create_question_api(client, endpoint, payload, expected_status):
    response = client.post(endpoint, data=json.dumps(payload), content_type="application/json")
    if response.status_code != expected_status:
        print("Response status:", response.status_code)
        print("Response body:", response.json())
    assert response.status_code == expected_status
