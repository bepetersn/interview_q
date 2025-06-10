from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from backend.infrastructure.tasks import import_questions
from backend.core.aws import publish_sqs_message
import logging

logger = logging.getLogger(__name__)


class ImportAPIView(APIView):
    def post(self, request, platform):
        username = request.data.get("username") if isinstance(request.data, dict) else None
        if not username:
            return Response({"error": "username required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if getattr(settings, "IMPORT_QUEUE_URL", None):
                resp = publish_sqs_message(
                    settings.IMPORT_QUEUE_URL,
                    "import_questions",
                    {"platform": platform, "username": username},
                )
                job_id = resp.get("MessageId")
            else:
                result = import_questions(platform, username)
                job_id = "local"
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.exception("Failed to queue import")
            return Response({"error": "failed to queue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.info("Queued import for %s", username)
        return Response({"job_id": job_id}, status=status.HTTP_202_ACCEPTED)

