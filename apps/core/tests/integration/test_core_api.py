import pytest
import json
import os
import logging
from apps.core.models import Question
from django.test import Client

logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api")


# Ensure valid test data setup

@pytest.fixture()
def setup_questions(db):
    # Create or retrieve questions with expected titles
    question1, _ = Question.objects.get_or_create(
        title="Two Sum", defaults={"slug": "two-sum"}
    )
    question2, _ = Question.objects.get_or_create(
        title="Binary Search", defaults={"slug": "binary-search"}
    )
    return question1.pk, question2.pk


@pytest.fixture()
def client():
    return Client()


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
)
@pytest.mark.django_db
def test_create_and_verify_question_log(client, setup_questions, payload, expected_title):
    question1_id, question2_id = setup_questions
    payload = dict(payload)
    payload["question"] = question1_id if expected_title == "Two Sum" else question2_id
    logger.info("Payload being sent: %s", json.dumps(payload, indent=2))
    assert ("question" in payload and payload["question"] is not None), "The 'question' field is missing or None in the payload."
    response = client.post(f"/api/questionlogs/", data=json.dumps(payload), content_type="application/json")
    logger.info("Response received: %s - %s", response.status_code, response.content)
    assert response.status_code == 201
    question_log_id = response.json().get("id")
    assert question_log_id is not None
    response = client.get(f"/api/questionlogs/{question_log_id}/")
    assert response.status_code == 200
    data = response.json()
    question_response = client.get(f"/api/questions/{data.get('question')}/")
    assert question_response.status_code == 200
    question_data = question_response.json()
    assert question_data.get("title") == expected_title
    response = client.delete(f"/api/questionlogs/{question_log_id}/")
    assert response.status_code == 204


@pytest.mark.parametrize("nonexistent_id", [99999, 88888])
@pytest.mark.django_db
def test_update_nonexistent_question_log(client, nonexistent_id):
    update_payload = {"title": "Nonexistent Log", "difficulty": "Hard"}
    response = client.patch(f"/api/questionlogs/{nonexistent_id}/", data=json.dumps(update_payload), content_type="application/json")
    assert response.status_code == 404
