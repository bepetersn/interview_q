import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

pytest_plugins = [
    "backend.fixtures",
]


@pytest.fixture(scope="session")
def django_server_url():
    """
    Provides the base URL for the Django live server for integration tests.
    """
    return "http://localhost:8000"
