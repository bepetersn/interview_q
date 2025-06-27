import os

from django.core.wsgi import get_wsgi_application

# Enable Datadog APM when requested
if os.getenv("DD_TRACE_ENABLED") == "true":
    try:
        import ddtrace.auto  # noqa: F401
    except Exception:
        pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

application = get_wsgi_application()
