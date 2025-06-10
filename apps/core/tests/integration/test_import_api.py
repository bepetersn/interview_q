import pytest
import json
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api")


@pytest.mark.parametrize(
    "platform, user_profile, expected_status",
    [
        ("leetcode", {"username": "test_user"}, 200),
        ("hackerrank", {"username": "test_user"}, 200),
        ("codewars", {"username": "test_user"}, 200),
        ("leetcode", {}, 400),
        ("hackerrank", None, 400),
        ("codewars", {"username": ""}, 400),
    ],
)
def test_import_questions(request_context, platform, user_profile, expected_status):
    # Simulate API call to import questions
    response = request_context.post(
        f"{API_URL}/import/{platform}/", data=json.dumps(user_profile)
    )
    assert response.status == expected_status


@pytest.mark.parametrize(
    "platform, api_response, expected_question_count",
    [
        ("leetcode", [{"title": "Two Sum", "difficulty": "Easy"}], 1),
        ("hackerrank", [{"title": "Binary Search", "difficulty": "Medium"}], 1),
        ("codewars", [], 0),
    ],
)
def test_data_mapping(request_context, platform, api_response, expected_question_count):
    # Mock external API response
    mock_api_url = f"{API_URL}/mock/{platform}/"
    request_context.post(mock_api_url, data=json.dumps(api_response))

    # Trigger import
    response = request_context.post(
        f"{API_URL}/import/{platform}/", data=json.dumps({"username": "test_user"})
    )
    assert response.status == 200

    # Verify imported data
    response = request_context.get(f"{API_URL}/questionlogs/")
    assert len(response.json()) == expected_question_count


@pytest.mark.parametrize(
    "platform, error_code",
    [
        ("leetcode", 500),
        ("hackerrank", 404),
        ("codewars", 408),
    ],
)
def test_error_handling(request_context, platform, error_code):
    # Simulate external API failure
    mock_api_url = f"{API_URL}/mock/{platform}/error/{error_code}/"
    request_context.post(mock_api_url)

    # Trigger import
    response = request_context.post(
        f"{API_URL}/import/{platform}/", data=json.dumps({"username": "test_user"})
    )
    assert response.status == 500
