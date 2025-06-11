import pytest
import json
import logging
import time
import requests
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


@pytest.fixture
def ensure_test_user(db):
    username = "apitestuser"
    password = "apitestpass"
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
    return username, password


@pytest.fixture()
def setup_questions():
    # Just provide question data, not DB objects
    return [
        {"title": "Two Sum"},
        {"title": "Binary Search"},
    ]


@pytest.fixture()
def api_session(django_server_url, ensure_test_user):
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    username, password = ensure_test_user
    resp = session.post(
        f"{django_server_url}/api/accounts/login/",
        json={"username": username, "password": password},
    )
    assert resp.status_code in (200, 201, 204), f"Auth failed: {resp.text}"
    csrf_token = session.cookies.get("csrftoken")
    if csrf_token:
        session.headers.update({"X-CSRFToken": csrf_token})
    return session, username


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected_title",
    [
        (
            {
                "time_spent_min": 15,
                "outcome": "Solved",
                "solution_approach": "Brute force",
                "self_notes": "Simple hash map",
                "question": None,  # Placeholder, will be set dynamically
            },
            "Two Sum",
        ),
        (
            {
                "time_spent_min": 30,
                "outcome": "Solved",
                "solution_approach": "Divide and conquer",
                "self_notes": "Efficient algorithm",
                "question": None,  # Placeholder, will be set dynamically
            },
            "Binary Search",
        ),
    ],
    ids=[
        "create log for Two Sum with brute force approach",
        "create log for Binary Search with divide and conquer approach",
    ],
)
def test_create_and_verify_question_log(
    api_session, setup_questions, payload, expected_title, django_server_url
):
    session, _ = api_session
    # Create questions via API and get their IDs
    q1_resp = session.post(
        f"{django_server_url}/api/questions/", json=setup_questions[0]
    )
    q2_resp = session.post(
        f"{django_server_url}/api/questions/", json=setup_questions[1]
    )
    assert q1_resp.status_code == 201
    assert q2_resp.status_code == 201
    question1_id = q1_resp.json()["id"]
    question2_id = q2_resp.json()["id"]
    payload = dict(payload)
    payload["question"] = question1_id if expected_title == "Two Sum" else question2_id
    logger.info("Payload being sent: %s", json.dumps(payload, indent=2))
    assert (
        "question" in payload and payload["question"] is not None
    ), "The 'question' field is missing or None in the payload."
    response = session.post(f"{django_server_url}/api/questionlogs/", json=payload)
    logger.info("Response received: %s - %s", response.status_code, response.content)
    assert response.status_code == 201
    question_log_id = response.json().get("id")
    assert question_log_id is not None
    response = session.get(f"{django_server_url}/api/questionlogs/{question_log_id}/")
    assert response.status_code == 200
    data = response.json()
    question_response = session.get(
        f"{django_server_url}/api/questions/{data.get('question')}/"
    )
    assert question_response.status_code == 200
    question_data = question_response.json()
    assert question_data.get("title") == expected_title
    response = session.delete(
        f"{django_server_url}/api/questionlogs/{question_log_id}/"
    )
    assert response.status_code == 204


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize(
    "nonexistent_id",
    [99999, 88888],
    ids=["nonexistent id 99999", "nonexistent id 88888"],
)
def test_update_nonexistent_question_log(
    api_session, nonexistent_id, setup_questions, django_server_url
):
    session, _ = api_session
    update_payload = {"title": "Nonexistent Log", "difficulty": "Hard"}
    response = session.patch(
        f"{django_server_url}/api/questionlogs/{nonexistent_id}/",
        json=update_payload,
    )
    assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.django_db
def test_list_scoped_to_user(api_session, setup_questions, django_server_url):
    session, _ = api_session
    # Create questions via API for the test user and get their IDs
    q1_resp = session.post(
        f"{django_server_url}/api/questions/", json=setup_questions[0]
    )
    assert q1_resp.status_code == 201
    q1_id = q1_resp.json()["id"]
    payload = {
        "question": q1_id,
        "time_spent_min": 10,
    }
    session.post(f"{django_server_url}/api/questionlogs/", json=payload)

    # create log for another user
    other_session = requests.Session()
    other_session.headers.update({"Content-Type": "application/json"})
    other_username = f"other_{int(time.time())}"
    # Register and login other user
    other_session.post(
        f"{django_server_url}/api/accounts/register/",
        json={"username": other_username, "password": "pass"},
    )
    other_session.post(
        f"{django_server_url}/api/accounts/login/",
        json={"username": other_username, "password": "pass"},
    )
    # Set CSRF token for other user session
    csrf_token = other_session.cookies.get("csrftoken")
    if csrf_token:
        other_session.headers.update({"X-CSRFToken": csrf_token})
    # Create the same question for the other user
    other_q1_resp = other_session.post(
        f"{django_server_url}/api/questions/", json=setup_questions[0]
    )
    assert other_q1_resp.status_code == 201
    other_q1_id = other_q1_resp.json()["id"]
    other_payload = {
        "question": other_q1_id,
        "time_spent_min": 10,
    }
    other_session.post(f"{django_server_url}/api/questionlogs/", json=other_payload)

    response = session.get(f"{django_server_url}/api/questionlogs/")
    assert response.status_code == 200
    assert len(response.json()) == 1
