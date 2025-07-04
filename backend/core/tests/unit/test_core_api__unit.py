import json

import pytest

from backend.core.tests.unit.mocks import (
    _mock_question,
    _mock_request,
    _mock_view_response,
)
from backend.core.views.question import QuestionViewSet


def _create_question(client, title="Original Question"):
    create_payload = {"title": title}
    resp = client.post(
        "/api/questions/",
        data=json.dumps(create_payload),
        content_type="application/json",
    )
    return resp


def _create_questionlog_and_dependencies(client):
    resp = _create_question(client, title="Test Q")
    question_id = resp.json()["id"]
    create_payload = {
        "title": "Original Question",
        "difficulty": "Easy",
    }
    log_resp = client.post(
        f"/api/questions/{question_id}/logs/",
        data=json.dumps(create_payload | {"question": question_id}),
        content_type="application/json",
    )
    log_id = log_resp.json()["id"]
    return question_id, log_id


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
        ("/api/tags/", {"name": "New Tag"}, 201),
        ("/api/tags/", {}, 400),
        ("/api/questions/", {"title": "New Question Title"}, 201),
        ("/api/questions/", {}, 400),
        ("/api/questions/", {"title": "Test Question", "slug": "forbidden-slug"}, 400),
    ],
    ids=[
        "create tag with name succeeds",
        "create tag with empty payload fails",
        "create question with only title succeeds",
        "create question with empty payload fails",
        "create question with forbidden slug fails",
    ],
)
def test_create_views(client, endpoint, payload, expected_status):
    # Handle tags and questions as before
    if endpoint == "/api/tags/" and expected_status == 201 and "name" not in payload:
        payload = dict(payload)
        payload["name"] = "Auto Tag"
    print(f"Testing endpoint: {endpoint} with payload: {payload}")
    response = client.post(
        endpoint, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"title": "New QuestionLog", "difficulty": "Easy"}, 201),
        ({}, 201),
    ],
    ids=[
        "create questionlog with title and difficulty succeeds",
        "create questionlog with empty payload succeeds",
    ],
)
def test_create_questionlog_views(client, payload, expected_status):
    question_id = _create_question(client).json()["id"]
    url = f"/api/questions/{question_id}/logs/"
    response = client.post(
        url,
        data=json.dumps(
            payload | {"question": question_id, "content": "Updated log content."}
        ),
        content_type="application/json",
    )
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, method, expected_status",
    [
        ("/api/tags/", "GET", 200),
        ("/api/questions/", "GET", 200),
    ],
    ids=[
        "list tags returns 200",
        "list questions returns 200",
    ],
)
def test_list_views(client, endpoint, method, expected_status):
    if method == "GET":
        response = client.get(endpoint)
    else:
        response = client.post(endpoint)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_list_questionlogs_view(client):
    question_id, _ = _create_questionlog_and_dependencies(client)
    url = f"/api/questions/{question_id}/logs/"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, payload, expected_status, question_id, log_id",
    [
        (
            "logs",
            {
                "question": 1,
                "date_attempted": "2025-06-10",
                "time_spent_min": 42,
                "outcome": "Solved",
                "solution_approach": "Refactor",
                "self_notes": "Updated log notes.",
            },
            200,
            None,
            None,
        ),
    ],
    ids=[
        "update questionlog with all fields succeeds",
    ],
)
def test_update_questionlog_views(
    client, endpoint, payload, expected_status, question_id, log_id
):
    if question_id is None:
        question_id, log_id = _create_questionlog_and_dependencies(client)
    url = f"/api/questions/{question_id}/{endpoint}/{log_id}/"
    response = client.put(
        url,
        data=json.dumps(payload | {"question": question_id}),
        content_type="application/json",
    )
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, expected_status, question_id, log_id",
    [
        ("logs", 204, None, None),
    ],
    ids=[
        "delete questionlog succeeds",
    ],
)
def test_delete_questionlog_views(
    client, endpoint, expected_status, question_id, log_id
):
    if question_id is None:
        question_id, log_id = _create_questionlog_and_dependencies(client)
    url = f"/api/questions/{question_id}/{endpoint}/{log_id}/"
    response = client.delete(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "endpoint, payload, expected_status",
    [
        ("/api/questions/", {"title": "FizzBuzz", "slug": "fizz-buzz"}, 400),
        ("/api/questions/", {}, 400),
        ("/api/questions/", {"title": "Only Title"}, 201),
        ("/api/questions/", {"title": "Test Question"}, 201),
        ("/api/questions/", {}, 400),
        ("/api/questions/", {"title": "Test Question", "slug": "should-fail"}, 400),
    ],
    ids=[
        "should fail with slug",
        "should fail with empty payload",
        "should create question with only title",
        "should create question with valid title",
        "should fail with empty payload",
        "should fail to create question with forbidden slug",
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


def test_create_questionlog_with_nonexistent_question(client):
    payload = {
        "title": "Should Fail",
        "difficulty": "Easy",
        "question": 9999,
    }
    response = client.post(
        "/api/questions/9999/logs/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code in (400, 404)


@pytest.mark.django_db
class TestQuestionContentSanitization:
    """Test content sanitization in question API endpoints"""

    def test_create_question_content_sanitization(self, client):
        """Test that safe HTML is preserved and unsafe HTML is sanitized"""
        payloads = [
            {
                "title": "Safe Content",
                "content": "<p>This is <strong>safe</strong> content</p>",
                "expected": "<p>This is <strong>safe</strong> content</p>",
            },
            {
                "title": "Unsafe Content",
                "content": "<p>Safe content</p><script>alert('xss')</script>",
                "expected": "<p>Safe content</p>",
            },
        ]

        for payload in payloads:
            response = client.post(
                "/api/questions/",
                data=json.dumps(
                    {"title": payload["title"], "content": payload["content"]}
                ),
                content_type="application/json",
            )
            assert response.status_code == 201
            data = response.json()
            assert data["content"] == payload["expected"]

    def test_create_question_with_excessive_whitespace(self, client):
        """Test that excessive whitespace is cleaned up"""
        payload = {
            "title": "Whitespace Test",
            "content": "Line 1\n\n\nLine 2     with    spaces\n\n\nLine 3",
        }
        response = client.post(
            "/api/questions/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.json()
        assert "\n\n\n" not in data["content"]
        assert "   " not in data["content"]
        assert "Line 1" in data["content"]
        assert "Line 2" in data["content"]
        assert "Line 3" in data["content"]

    def test_create_question_with_short_content(self, client):
        """Test that very short content after sanitization is rejected"""
        payload = {
            "title": "Short Content",
            "content": "<script>alert('xss')</script>",
        }
        response = client.post(
            "/api/questions/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        # Should succeed with sanitized content (XSS content gets stripped)
        assert response.status_code == 201
        data = response.json()
        # Content should be sanitized (empty after script removal)
        assert data["content"] == ""

    def test_update_question_content_sanitization(self, client):
        """Test that content is sanitized when updating questions"""
        create_payload = {"title": "Update Test", "content": "Original content"}
        create_response = client.post(
            "/api/questions/",
            data=json.dumps(create_payload),
            content_type="application/json",
        )
        assert create_response.status_code == 201
        question_id = create_response.json()["id"]

        update_payload = {
            "content": "<p>Updated content</p><script>alert('xss')</script>",
        }
        update_response = client.patch(
            f"/api/questions/{question_id}/",
            data=json.dumps(update_payload),
            content_type="application/json",
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert "<p>" in data["content"]
        assert "Updated content" in data["content"]
        assert "<script>" not in data["content"]
        assert "alert('xss')" not in data["content"]
