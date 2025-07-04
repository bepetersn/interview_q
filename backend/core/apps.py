from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.core"

    def ready(self):
        """Import signal handlers when the app is ready."""
        # Import signals to ensure they are registered
        from . import signals  # noqa: F401
