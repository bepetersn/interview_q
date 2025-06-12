import time
import pytest
import json
import logging
import requests
from backend.fixtures import BASE_URL, create_and_cleanup_user

logger = logging.getLogger(__name__)


@pytest.fixture()
def setup_questions():
    return [
        {"title": "Two Sum"},
        {"title": "Binary Search"},
    ]


def _create_user_and_session(username, password):
    session = requests.Session()
    resp = session.post(
        f"{BASE_URL}/accounts/register/",
        json={"username": username, "password": password},
    )
    assert resp.status_code in (200, 201, 204)
    resp = session.post(
        f"{BASE_URL}/accounts/login/",
        json={"username": username, "password": password},
    )
    assert resp.status_code in (200, 201, 204)
    csrf_token = session.cookies.get("csrftoken")
    if csrf_token:
        session.headers.update({"X-CSRFToken": csrf_token})
    return session


@pytest.fixture()
def cleanup_main_user_questions(logged_in_session):
    session, _ = logged_in_session
    question_api = f"{BASE_URL}/questions/"
    # Delete all questions for the user (logs will be deleted via cascade)
    questions = session.get(question_api).json()
    for q in questions:
        session.delete(f"{question_api}{q['id']}/")


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
                "question": None,
            },
            "Two Sum",
        ),
        (
            {
                "time_spent_min": 30,
                "outcome": "Solved",
                "solution_approach": "Divide and conquer",
                "self_notes": "Efficient algorithm",
                "question": None,
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
    ensure_server, logged_in_session, setup_questions, payload, expected_title
):
    session, _ = logged_in_session
    # Create questions via API and get their IDs
    q1_resp = session.post(f"{BASE_URL}/questions/", json=setup_questions[0])
    q2_resp = session.post(f"{BASE_URL}/questions/", json=setup_questions[1])
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
    response = session.post(f"{BASE_URL}/questionlogs/", json=payload)
    logger.info("Response received: %s - %s", response.status_code, response.content)
    assert response.status_code == 201
    question_log_id = response.json().get("id")
    assert question_log_id is not None
    response = session.get(f"{BASE_URL}/questionlogs/{question_log_id}/")
    assert response.status_code == 200
    data = response.json()
    question_response = session.get(f"{BASE_URL}/questions/{data.get('question')}/")
    assert question_response.status_code == 200
    question_data = question_response.json()
    assert question_data.get("title") == expected_title
    response = session.delete(f"{BASE_URL}/questionlogs/{question_log_id}/")
    assert response.status_code == 204


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize(
    "nonexistent_id",
    [99999, 88888],
    ids=["nonexistent id 99999", "nonexistent id 88888"],
)
def test_update_nonexistent_question_log(
    logged_in_session, nonexistent_id, setup_questions
):
    session, _ = logged_in_session
    update_payload = {"title": "Nonexistent Log", "difficulty": "Hard"}
    response = session.patch(
        f"{BASE_URL}/api/questionlogs/{nonexistent_id}/",
        json=update_payload,
    )
    assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.django_db
def test_list_scoped_to_user(
    logged_in_session, setup_questions, cleanup_main_user_questions
):
    main_session, _ = logged_in_session
    question_api = f"{BASE_URL}/questions/"
    questionlog_api = f"{BASE_URL}/questionlogs/"

    # Create a question and log for the main test user
    q1_resp = main_session.post(question_api, json=setup_questions[0])
    assert q1_resp.status_code == 201
    q1_id = q1_resp.json()["id"]
    payload = {"question": q1_id, "time_spent_min": 10}
    log_resp = main_session.post(questionlog_api, json=payload)
    assert log_resp.status_code == 201

    # Create another user and add a question log for them
    other_username = "other" + str(int(time.time()))
    other_password = "pass"
    other_session, other_cleanup = create_and_cleanup_user(
        other_username, other_password
    )
    other_q_id = None
    try:
        other_q_resp = other_session.post(question_api, json=setup_questions[0])
        assert other_q_resp.status_code == 201
        other_q_id = other_q_resp.json()["id"]
        other_payload = {"question": other_q_id, "time_spent_min": 10}
        other_log_resp = other_session.post(questionlog_api, json=other_payload)
        assert other_log_resp.status_code == 201

        # Ensure only the test user's log is returned
        response = main_session.get(questionlog_api)
        assert response.status_code == 200
        logs = response.json()
        assert isinstance(logs, list)
        assert len(logs) == 1
        assert logs[0]["question"] == q1_id
    finally:
        if other_q_id:
            # Ensure the other user's question/questionlog is cleaned up
            other_session.delete(f"{question_api}{other_q_id}/")
        other_cleanup()


@pytest.mark.integration
@pytest.mark.django_db
def test_question_retrieve_update_destroy(logged_in_session, setup_questions):
    session, _ = logged_in_session
    # Create a question
    q_resp = session.post(f"{BASE_URL}/questions/", json=setup_questions[0])
    assert q_resp.status_code == 201
    q_id = q_resp.json()["id"]

    # Retrieve the question
    retrieve_resp = session.get(f"{BASE_URL}/questions/{q_id}/")
    assert retrieve_resp.status_code == 200
    data = retrieve_resp.json()
    assert data["id"] == q_id
    assert data["title"] == setup_questions[0]["title"]

    # Update the question
    update_payload = {"title": "Updated Title"}
    update_resp = session.patch(f"{BASE_URL}/questions/{q_id}/", json=update_payload)
    assert update_resp.status_code == 200
    updated_data = update_resp.json()
    assert updated_data["title"] == "Updated Title"

    # Destroy the question
    destroy_resp = session.delete(f"{BASE_URL}/questions/{q_id}/")
    assert destroy_resp.status_code == 204

    # Ensure it is gone
    gone_resp = session.get(f"{BASE_URL}/questions/{q_id}/")
    assert gone_resp.status_code == 404
