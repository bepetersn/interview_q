import pytest
import requests
import time
import subprocess
import socket
import os
import sqlite3

# flake8: noqa

BASE_URL = "http://localhost:8000/api"


def is_server_running(host="localhost", port=8000):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def wait_for_server(host="localhost", port=8000, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        if is_server_running(host, port):
            return True
        time.sleep(0.5)
    return False


@pytest.fixture(scope="function")
def e2e_test_user():
    username = f"e2euser_{int(time.time())}"
    password = "e2epass123"
    session = requests.Session()
    # Register
    resp = session.post(
        f"{BASE_URL}/accounts/register/",
        json={"username": username, "password": password},
    )
    assert resp.status_code in (200, 201, 204), f"Register failed: {resp.text}"
    yield session, username, password
    # Cleanup
    try:
        session.post(
            f"{BASE_URL}/accounts/delete/",
            json={"username": username, "password": password},
        )
    except Exception as cleanup_exc:
        print(f"Cleanup failed: {cleanup_exc}")


@pytest.mark.parametrize("_", [None], ids=["auth-end-to-end-flow"])
def test_auth_end_to_end(_, e2e_test_user):
    server_proc = None
    if not is_server_running():
        # Start Django dev server
        server_proc = subprocess.Popen(
            ["python", "manage.py", "runserver", "0.0.0.0:8000"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")),
        )
        assert wait_for_server(), "Django server did not start in time."
    session, username, password = e2e_test_user
    try:
        # Login
        resp = session.post(
            f"{BASE_URL}/accounts/login/",
            json={"username": username, "password": password},
        )
        assert resp.status_code in (200, 201, 204), f"Login failed: {resp.text}"

        # Access protected endpoint
        resp = session.get(f"{BASE_URL}/questions/")
        assert resp.status_code == 200, f"Protected endpoint failed: {resp.text}"

        # Logout (with CSRF token)
        csrf_token = session.cookies.get("csrftoken")
        headers = {"X-CSRFToken": csrf_token} if csrf_token else {}
        resp = session.post(f"{BASE_URL}/accounts/logout/", headers=headers)
        assert resp.status_code in (200, 201, 204), f"Logout failed: {resp.text}"
    finally:
        if server_proc:
            server_proc.terminate()
            server_proc.wait()
