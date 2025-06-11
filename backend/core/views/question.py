from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from ..models import Question
from ..serializers import QuestionSerializer
import logging
from rest_framework.exceptions import ValidationError


class QuestionExceptionMixin:
    def handle_request_with_logging(self, action, request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info(f"Entering the {action} method for Question")
        logger.info(f"Incoming payload: {request.data}")
        try:
            super_method = getattr(super(), action)
            response = super_method(request, *args, **kwargs)
        except ValidationError as exc:
            logger.warning(f"Validation error {action} Question: {exc}")
            return Response(exc.detail, status=400)
        except Exception as exc:
            logger.error(f"Unexpected error {action} Question: {exc}")
            return Response({"error": str(exc)}, status=500)
        expected_status = 201 if action == "create" else 200
        if response.status_code != expected_status:
            logger.error(f"Error {action} Question: {response.data}")
        return response


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        # Return type "BaseManager[Question]" is not
        # assignable to type "Never" in base class
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionListCreateView(QuestionExceptionMixin, generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return self.handle_request_with_logging("create", request, *args, **kwargs)
