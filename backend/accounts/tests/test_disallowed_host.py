import pytest
from django.test import override_settings, Client

# flake8: noqa


@pytest.mark.parametrize("_", [None], ids=["disallowed-host-returns-400"])
@override_settings(ALLOWED_HOSTS=["example.com"])
def test_disallowed_host(_):
    client = Client()
    resp = client.get("/", HTTP_HOST="notallowed.com")
    assert resp.status_code == 400
