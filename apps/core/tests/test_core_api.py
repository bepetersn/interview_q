import pytest
import json
import os
import logging
from django.core.management import call_command
from apps.core.models import Question

logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api")

# Ensure the database is populated with test data
call_command("create_fake_data")

# Retrieve a valid Question ID for testing
question_id = Question.objects.first().id if Question.objects.exists() else None


# Ensure valid test data setup
@pytest.fixture(scope="module")
def setup_questions():
    # Create or retrieve questions with expected titles
    question1, _ = Question.objects.get_or_create(
        title="Two Sum", defaults={"slug": "two-sum"}
    )
    question2, _ = Question.objects.get_or_create(
        title="Binary Search", defaults={"slug": "binary-search"}
    )
    return question1.pk, question2.pk


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
def test_create_and_verify_question_log(
    request_context, setup_questions, payload, expected_title
):
    question1_id, question2_id = setup_questions

    # Dynamically set the question ID in the payload
    payload["question"] = question1_id if expected_title == "Two Sum" else question2_id

    # Log the payload being sent
    logger.info("Payload being sent: %s", json.dumps(payload, indent=2))

    # Ensure the 'question' field is included
    assert (
        "question" in payload and payload["question"] is not None
    ), "The 'question' field is missing or None in the payload."

    # Create a question log
    response = request_context.post(
        f"{API_URL}/questionlogs/", data=json.dumps(payload)
    )

    # Log the response received
    logger.info("Response received: %s - %s", response.status, response.text)

    assert response.status == 201

    # Retrieve the created question log ID
    question_log_id = response.json().get("id")
    assert question_log_id is not None

    # Verify the created question log
    response = request_context.get(f"{API_URL}/questionlogs/{question_log_id}/")
    assert response.status == 200
    data = response.json()

    # Verify the title of the related Question object
    question_response = request_context.get(
        f"{API_URL}/questions/{data.get('question')}/"
    )
    assert question_response.status == 200
    question_data = question_response.json()
    assert question_data.get("title") == expected_title

    # Clean up by deleting the question log
    response = request_context.delete(f"{API_URL}/questionlogs/{question_log_id}/")
    assert response.status == 204


@pytest.mark.parametrize("nonexistent_id", [99999, 88888])
def test_update_nonexistent_question_log(request_context, nonexistent_id):
    # Attempt to update a non-existent question log
    update_payload = {"title": "Nonexistent Log", "difficulty": "Hard"}
    response = request_context.patch(
        f"{API_URL}/questionlogs/{nonexistent_id}/", data=json.dumps(update_payload)
    )

    # Assert that the response status is 404
    assert response.status == 404
