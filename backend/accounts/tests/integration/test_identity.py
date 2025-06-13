from fixtures import BASE_URL, REQUESTS_VERIFY
import pytest

# flake8: noqa


def test_identity_unauthenticated(ensure_server):
    import requests

    resp = requests.get(f"{BASE_URL}/accounts/identity/", verify=False)
    assert resp.status_code == 200
    data = resp.json()
    assert data["authenticated"] is False
    assert data["user"] is None


def test_identity_authenticated(ensure_server, registered_user):
    session, username, _ = registered_user
    # Login
    resp = session.post(
        f"{BASE_URL}/accounts/login/",
        json={"username": username, "password": "apitestpass"},
        verify=REQUESTS_VERIFY,
    )
    assert resp.status_code in (200, 201, 204)
    # Identity
    resp = session.get(f"{BASE_URL}/accounts/identity/", verify=REQUESTS_VERIFY)
    assert resp.status_code == 200
    data = resp.json()
    assert data["authenticated"] is True
    assert data["user"]["username"] == username
    assert "id" in data["user"]
    assert "email" in data["user"]
    assert "is_superuser" in data["user"]
    assert "is_staff" in data["user"]
