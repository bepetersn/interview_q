from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import logging
from ..models import QuestionLog
from ..serializers import QuestionLogSerializer

logger = logging.getLogger(__name__)


class QuestionLogExceptionMixin:
    def handle_request_with_logging(self, action, request, *args, **kwargs):
        logger.info(f"Entering the {action} method for QuestionLog")
        logger.info(f"Incoming payload: {request.data}")
        try:
            super_method = getattr(super(), action)
            response = super_method(request, *args, **kwargs)
        except ValidationError as exc:
            logger.warning(f"Validation error {action} QuestionLog: {exc}")
            return Response(exc.detail, status=400)
        except Exception as exc:
            logger.error(f"Unexpected error {action} QuestionLog: {exc}")
            return Response({"error": str(exc)}, status=500)

        expected_status = 201 if action == "create" else 200
        if response.status_code != expected_status:
            logger.error(f"Error {action} QuestionLog: {response.data}")
        return response


class QuestionLogViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return QuestionLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionLogListCreateView(QuestionLogExceptionMixin, generics.ListCreateAPIView):
    serializer_class = QuestionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return QuestionLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return self.handle_request_with_logging("create", request, *args, **kwargs)


class QuestionLogRetrieveUpdateDestroyView(
    QuestionLogExceptionMixin, generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = QuestionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return QuestionLog.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            self.get_object()
        except Exception as exc:
            logger.warning(f"Object not found for update: {exc}")
            return Response({"detail": "Not found."}, status=404)
        return self.handle_request_with_logging("update", request, *args, **kwargs)
