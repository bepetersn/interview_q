import pytest
from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture(scope="function")
def reset_database():
    """
    Reset the database after a test using Django's flush command for a clean
    and fast state. Use only for tests that require a completely clean DB.
    """
    call_command("flush", verbosity=0, interactive=False)


@pytest.fixture()
def user(db):
    return User.objects.create_user(username="slugtestuser", password="pass")


@pytest.fixture()
def client(user):
    client = Client()
    client.login(username="slugtestuser", password="pass")
    return client
