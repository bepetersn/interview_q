# flake8: noqa
import json

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected_status, slug_check",
    [
        # User supplies a slug, should fail
        ({"title": "Unique Slug Test", "slug": "user-supplied-slug"}, 400, None),
        # User omits slug, API should generate one
        ({"title": "Another Slug Test"}, 201, "another-slug-test"),
        # User supplies only slug, should fail (title required)
        ({"slug": "should-not-work"}, 400, None),
    ],
    ids=[
        "fail with user-supplied slug",
        "create and generate slug",
        "fail with only slug",
    ],
)
def test_question_api_slug_handling(client, payload, expected_status, slug_check):
    response = client.post(
        "/api/questions/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == expected_status
    if expected_status == 201 and slug_check:
        data = response.json()
        assert data["slug"] is not None and data["slug"] != ""
        assert slug_check in data["slug"]
