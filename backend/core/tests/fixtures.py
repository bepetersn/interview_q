import pytest
from playwright.sync_api import sync_playwright
import sqlite3
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture(scope="function")
def request_context():
    with sync_playwright() as p:
        context = p.request.new_context(
            extra_http_headers={"Content-Type": "application/json"}
        )
        yield context
        context.dispose()


@pytest.fixture(scope="function", autouse=True)
def reset_database():
    # Reset the SQLite database after each test
    db_path = "backend/db/db.sqlite3"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM core_questionlog")
    connection.commit()
    connection.close()


@pytest.fixture()
def user(db):
    return User.objects.create_user(username="slugtestuser", password="pass")


@pytest.fixture()
def client(user):
    client = Client()
    client.login(username="slugtestuser", password="pass")
    return client
