import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

pytest_plugins = [
    "backend.test_common.fixtures",
]


@pytest.fixture(scope="session")
def django_server_url():
    """
    Provides the base URL for the Django live server for integration tests.
    """
    return "https://127.0.0.1:8000"
