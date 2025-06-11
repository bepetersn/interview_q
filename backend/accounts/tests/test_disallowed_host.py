import pytest
from django.test import override_settings, Client

# flake8: noqa


@override_settings(ALLOWED_HOSTS=["example.com"])
def test_disallowed_host():
    client = Client()
    resp = client.get("/", HTTP_HOST="notallowed.com")
    assert resp.status_code == 400
