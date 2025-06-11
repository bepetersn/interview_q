import pytest
import json
import os

API_URL = os.getenv("API_URL", "/api")  # Use relative path for Django test client


@pytest.mark.django_db
@pytest.mark.xfail(reason="Import API is not stable or not implemented yet.")
def test_import_questions(client, reset_database):
    test_cases = [
        ("codewars", {"username": "test_user"}, 200),
        ("codewars", {"username": ""}, 400),
    ]
    for platform, user_profile, expected_status in test_cases:
        data = json.dumps(user_profile) if user_profile is not None else None
        response = client.post(
            f"{API_URL}/import/{platform}/", data=data, content_type="application/json"
        )
        assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.xfail(reason="Import API is not stable or not implemented yet.")
def test_data_mapping(client, reset_database):
    test_cases = [
        ("codewars", [], 0),
    ]
    for platform, api_response, expected_question_count in test_cases:
        mock_api_url = f"{API_URL}/mock/{platform}/"
        client.post(
            mock_api_url, data=json.dumps(api_response), content_type="application/json"
        )
        response = client.post(
            f"{API_URL}/import/{platform}/",
            data=json.dumps({"username": "test_user"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        response = client.get(f"{API_URL}/questionlogs/")
        assert len(response.json()) == expected_question_count


@pytest.mark.django_db
@pytest.mark.xfail(reason="Import API is not stable or not implemented yet.")
def test_error_handling(client, reset_database):
    test_cases = [
        ("codewars", 408),
    ]
    for platform, error_code in test_cases:
        mock_api_url = f"{API_URL}/mock/{platform}/error/{error_code}/"
        client.post(mock_api_url)
        response = client.post(
            f"{API_URL}/import/{platform}/",
            data=json.dumps({"username": "test_user"}),
            content_type="application/json",
        )
        assert response.status_code == 500
