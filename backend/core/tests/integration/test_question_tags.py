import json

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from backend.core.models import Question, Tag


@pytest.mark.integration
@pytest.mark.django_db
def test_question_update_with_tag_ids():
    """Test updating a question with tag_ids"""
    # Create a test client
    client = Client()

    # Create a test user
    user_model = get_user_model()
    user = user_model.objects.create_user(username="testuser_tags", password="testpass")

    # Clean up existing data for this user
    Question.objects.filter(user=user).delete()
    Tag.objects.filter(user=user).delete()

    # Create some test tags
    tag1 = Tag.objects.create(name="Algorithm", user=user)
    tag2 = Tag.objects.create(name="Hard", user=user)
    tag3 = Tag.objects.create(name="Array", user=user)

    # Login the user (simulate authentication)
    client.force_login(user)

    # Create a test question
    question_data = {
        "title": "Test Question",
        "source": "Test Platform",
        "notes": "Test notes",
        "difficulty": "Hard",
        "tag_ids": [tag1.pk, tag2.pk],
    }

    create_response = client.post(
        "/api/questions/",
        data=json.dumps(question_data),
        content_type="application/json",
    )

    assert create_response.status_code == 201
    question_id = create_response.json()["id"]
    question = Question.objects.get(id=question_id)
    assert question.tags.count() == 2

    # Update the question with different tag_ids
    update_data = {
        "title": "Updated Test Question",
        "tag_ids": [tag2.pk, tag3.pk],  # Change tags
    }

    update_response = client.put(
        f"/api/questions/{question_id}/",
        data=json.dumps(update_data),
        content_type="application/json",
    )

    assert update_response.status_code == 200

    # Refresh the question from database
    question.refresh_from_db()
    updated_tag_ids = list(question.tags.values_list("id", flat=True))

    # Check if the tags were updated correctly
    expected_tag_ids = [tag2.pk, tag3.pk]
    assert set(updated_tag_ids) == set(
        expected_tag_ids
    ), f"Expected tags {expected_tag_ids}, got {updated_tag_ids}"
