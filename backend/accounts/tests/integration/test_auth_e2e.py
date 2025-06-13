from fixtures import BASE_URL, REQUESTS_VERIFY

# flake8: noqa


def test_auth_end_to_end(ensure_server, registered_user):
    session, username, password = registered_user
    # Login
    resp = session.post(
        f"{BASE_URL}/accounts/login/",
        json={"username": username, "password": password},
        verify=REQUESTS_VERIFY,
    )
    assert resp.status_code in (200, 201, 204), f"Login failed: {resp.text}"

    # Access protected endpoint
    resp = session.get(f"{BASE_URL}/questions/", verify=REQUESTS_VERIFY)
    assert resp.status_code == 200, f"Protected endpoint failed: {resp.text}"

    # Logout (with CSRF token)
    csrf_token = session.cookies.get("csrftoken")
    headers = {"X-CSRFToken": csrf_token} if csrf_token else {}
    # Add Referer header to satisfy CSRF checks
    headers["Referer"] = BASE_URL
    resp = session.post(
        f"{BASE_URL}/accounts/logout/", headers=headers, verify=REQUESTS_VERIFY
    )
    assert resp.status_code in (200, 201, 204), f"Logout failed: {resp.text}"
