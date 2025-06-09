import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

pytest_plugins = ["apps.core.tests.fixtures"]
