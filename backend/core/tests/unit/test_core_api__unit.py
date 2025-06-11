import pytest
import json
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture()
def user(db):
    return User.objects.create_user(username="tester", password="pass")


@pytest.fixture()
def client(user):
    client = Client()
    client.login(username="tester", password="pass")
    return client


def _create_questionlog_and_dependencies(client):
    # Ensure a question exists for the foreign key
    question_payload = {"title": "Test Q", "slug": "test-q", "difficulty": "Easy"}
    resp = client.post(
        "/api/questions/",
        data=json.dumps(question_payload),
        content_type="application/json",
    )
    question_id = resp.json()["id"]
    create_payload = {"title": "Original Question", "difficulty": "Easy", "question": question_id}
    client.post(
        "/api/questionlogs/",
        data=json.dumps(create_payload),
        content_type="application/json",
    )


def _create_tag(client):
    create_payload = {"name": "Original Tag"}
    client.post(
        "/api/tags/", data=json.dumps(create_payload), content_type="application/json"
    )


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
            "difficulty": "Easy",
        }
        question_response = client.post(
            "/api/questions/",
            data=json.dumps(question_payload),
            content_type="application/json",
        )
        assert question_response.status_code == 201
        question_id = question_response.json()["id"]
        payload = dict(payload)
        payload["question"] = question_id
    # If testing tags, ensure 'name' is present for 201
    if endpoint == "/api/tags/" and expected_status == 201 and "name" not in payload:
        payload = dict(payload)
        payload["name"] = "Auto Tag"
    response = client.post(
        endpoint, data=json.dumps(payload), content_type="application/json"
    )
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
def test_user_scoped_list(client):
    _create_questionlog_and_dependencies(client)
    from django.contrib.auth.models import User

    other = User.objects.create_user(username="other", password="pass")
    other_client = Client()
    other_client.login(username="other", password="pass")
    question_payload = {"title": "Q2", "slug": "q2", "difficulty": "Easy"}
    resp = other_client.post(
        "/api/questions/",
        data=json.dumps(question_payload),
        content_type="application/json",
    )
    other_client.post(
        "/api/questionlogs/",
        data=json.dumps({"question": resp.json()["id"]}),
        content_type="application/json",
    )

    response = client.get("/api/questionlogs/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, payload, expected_status",
    [
        (
            "/api/questionlogs/1/",
            {
                # Only fields allowed to be updated on QuestionLog
                "question": 1,  # required field
                "date_attempted": "2025-06-10",
                "time_spent_min": 42,
                "outcome": "Solved",
                "solution_approach": "Refactor",
                "self_notes": "Updated log notes.",
            },
            200,
        ),
        # Remove tag update test, as tag update is no longer supported
    ],
)
def test_update_views(client, endpoint, payload, expected_status):
    if endpoint.startswith("/api/questionlogs/"):
        _create_questionlog_and_dependencies(client)
    response = client.put(
        endpoint, data=json.dumps(payload), content_type="application/json"
    )
    if endpoint.startswith("/api/questionlogs/"):
        get_response = client.get(endpoint)
        assert get_response.status_code == 200
        data = get_response.json()
        for key, value in payload.items():
            if key == "date_attempted":
                # The API returns ISO datetime, but the test payload is a date string
                assert data[key].startswith(value)
            else:
                assert data[key] == value
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, expected_status",
    [
        ("/api/questionlogs/1/", 204),
        ("/api/tags/1/", 204),
        ("/api/questions/1/", 204),
    ],
)
def test_delete_views(client, endpoint, expected_status):
    if endpoint.startswith("/api/questionlogs/"):
        _create_questionlog_and_dependencies(client)
    elif endpoint.startswith("/api/tags/"):
        _create_tag(client)
    elif endpoint.startswith("/api/questions/"):
        question_payload = {
            "title": "Delete Me",
            "slug": "delete-me",
        }
        client.post(
            "/api/questions/",
            data=json.dumps(question_payload),
            content_type="application/json",
        )
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
    response = client.post(
        endpoint, data=json.dumps(payload), content_type="application/json"
    )
    if response.status_code != expected_status:
        print("Response status:", response.status_code)
        print("Response body:", response.json())
    assert response.status_code == expected_status
