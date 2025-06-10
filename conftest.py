import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

pytest_plugins = ["backend.core.tests.fixtures"]
