import os
import socket
import subprocess
import time

import pytest
import requests
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client

BASE_URL = "https://127.0.0.1:8000/api"

REQUESTS_VERIFY = (
    False  # Set to False to disable SSL verification globally for local/dev
)


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
def ensure_server():
    server_proc = None
    if not is_server_running():
        server_proc = subprocess.Popen(
            ["python", "manage.py", "runserver", "0.0.0.0:8000"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        )
        assert wait_for_server(), "Django server did not start in time."
    yield
    if server_proc:
        server_proc.terminate()
        server_proc.wait()


@pytest.fixture(scope="function")
def registered_user(db):
    username = "apitestuser"
    password = "apitestpass"
    session = requests.Session()
    try:
        # Attempt to register via API; ignore errors if user already exists
        reg_resp = session.post(
            f"{BASE_URL}/accounts/register/",
            json={"username": username, "password": password},
            verify=REQUESTS_VERIFY,
        )
        reg_resp.raise_for_status()
    except requests.exceptions.HTTPError:
        pass

    yield session, username, password


@pytest.fixture()
def logged_in_session(django_server_url, registered_user):
    session, username, password = registered_user
    session.headers.update({"Content-Type": "application/json"})
    resp = session.post(
        f"{django_server_url}/api/accounts/login/",
        json={"username": username, "password": password},
        verify=REQUESTS_VERIFY,
    )
    assert resp.status_code in (200, 201, 204), f"Auth failed: {resp.text}"
    csrf_token = session.cookies.get("csrftoken")
    if csrf_token:
        # Use https://localhost:8000 as the Referer to match BASE_URL domain
        session.headers.update(
            {"X-CSRFToken": csrf_token, "Referer": "https://localhost:8000"}
        )
    return session, username


@pytest.fixture(scope="function")
def reset_database():
    call_command("flush", verbosity=0, interactive=False)


@pytest.fixture()
def user(db):
    return User.objects.create_user(username="slugtestuser", password="pass")


@pytest.fixture()
def client(user):
    client = Client()
    client.login(username="slugtestuser", password="pass")
    return client


def create_and_cleanup_user(username, password):
    session = requests.Session()
    resp = session.post(
        f"{BASE_URL}/accounts/register/",
        json={"username": username, "password": password},
        verify=REQUESTS_VERIFY,
    )
    assert resp.status_code in (200, 201, 204), f"Register failed: {resp.text}"
    resp = session.post(
        f"{BASE_URL}/accounts/login/",
        json={"username": username, "password": password},
        verify=REQUESTS_VERIFY,
    )
    assert resp.status_code in (200, 201, 204), f"Login failed: {resp.text}"
    csrf_token = session.cookies.get("csrftoken")
    if csrf_token:
        session.headers.update({"X-CSRFToken": csrf_token, "Referer": BASE_URL})

    def cleanup():
        try:
            session.post(
                f"{BASE_URL}/accounts/delete/",
                json={"username": username, "password": password},
                verify=REQUESTS_VERIFY,
            )
        except Exception as cleanup_exc:
            print(f"Cleanup failed for {username}: {cleanup_exc}")

    return session, cleanup
