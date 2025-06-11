import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

pytest_plugins = [
    "backend.core.tests.fixtures",
]


@pytest.fixture(scope="session")
def django_server_url(live_server):
    """
    Provides the base URL for the Django live server for integration tests.
    """
    return live_server.url
