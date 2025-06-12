import pytest
import json
from backend.core.views.question import QuestionViewSet
from backend.core.tests.unit.mocks import (
    _mock_question,
    _mock_request,
    _mock_view_response,
)


def _create_questionlog_and_dependencies(client):
    # Ensure a question exists for the foreign key
    question_payload = {"title": "Test Q", "difficulty": "Easy"}
    resp = client.post(
        "/api/questions/",
        data=json.dumps(question_payload),
        content_type="application/json",
    )
    question_id = resp.json()["id"]
    create_payload = {
        "title": "Original Question",
        "difficulty": "Easy",
        "question": question_id,
    }
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


class _OpenQuestionViewSet(QuestionViewSet):
    """Subclass the viewset for open permissions in unit tests"""

    permission_classes = []


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, payload, expected_status",
    [
        ("/api/questionlogs/", {"title": "New Question", "difficulty": "Easy"}, 400),
        ("/api/questionlogs/", {}, 400),
        ("/api/tags/", {"name": "New Tag"}, 201),
        ("/api/tags/", {}, 400),
    ],
    ids=[
        "create questionlog with title and difficulty fails",
        "create questionlog with empty payload fails",
        "create tag with name succeeds",
        "create tag with empty payload fails",
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
    ids=[
        "list questionlogs returns 200",
        "list tags returns 200",
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
    ],
    ids=[
        "update questionlog with all fields succeeds",
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
    ids=[
        "delete questionlog succeeds",
        "delete tag succeeds",
        "delete question succeeds",
    ],
)
def test_delete_views(client, endpoint, expected_status):
    if endpoint.startswith("/api/questionlogs/"):
        _create_questionlog_and_dependencies(client)
    elif endpoint.startswith("/api/tags/"):
        _create_tag(client)
    elif endpoint.startswith("/api/questions/"):
        question_payload = {"title": "Delete Me"}
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
        ("/api/questions/", {"title": "FizzBuzz", "slug": "fizz-buzz"}, 400),
        ("/api/questions/", {}, 400),
        ("/api/questions/", {"title": "Only Title"}, 201),
    ],
    ids=[
        "should fail with slug",
        "should fail with empty payload",
        "should create question with only title",
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


def test_question_retrieve_unit():
    mock_question = _mock_question(123, "Retrieve Me")
    request = _mock_request("get", "/api/questions/123/")
    response = _mock_view_response(
        viewset_cls=_OpenQuestionViewSet,
        action_map={"get": "retrieve"},
        request=request,
        pk=123,
        mock_obj=mock_question,
        serializer_data={"id": 123, "title": "Retrieve Me"},
    )
    assert response.status_code == 200
    assert response.data["id"] == 123
    assert response.data["title"] == "Retrieve Me"


def test_question_update_unit():
    mock_question = _mock_question(456, "Update Me")
    update_payload = {"title": "Updated Title"}
    request = _mock_request("patch", "/api/questions/456/", data=update_payload)
    response = _mock_view_response(
        viewset_cls=_OpenQuestionViewSet,
        action_map={"patch": "partial_update"},
        request=request,
        pk=456,
        mock_obj=mock_question,
        serializer_data={"id": 456, "title": "Updated Title"},
    )
    assert response.status_code == 200
    assert response.data["title"] == "Updated Title"


def test_question_delete_unit():
    mock_question = _mock_question(789, "", delete=True)
    request = _mock_request("delete", "/api/questions/789/")
    response = _mock_view_response(
        viewset_cls=_OpenQuestionViewSet,
        action_map={"delete": "destroy"},
        request=request,
        pk=789,
        mock_obj=mock_question,
    )
    assert response.status_code in (204, 200)
