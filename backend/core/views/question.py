from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from ..models import Question
from ..serializers import QuestionSerializer
import logging
from rest_framework.exceptions import ValidationError


class QuestionExceptionMixin:

    def handle_request_with_logging_dispatch(
        self, dispatch_func, request, *args, **kwargs
    ):
        logger = logging.getLogger(__name__)
        logger.info(f"Dispatching {request.method} {request.path} for Question")
        logger.info(f"Incoming payload: {getattr(request, 'data', None)}")
        try:
            response = dispatch_func(request, *args, **kwargs)
        except ValidationError as exc:
            logger.warning(f"Validation error during dispatch: {exc}")
            return Response(exc.detail, status=400)
        except Exception as exc:
            logger.error(f"Unexpected error during dispatch: {exc}")
            return Response({"error": str(exc)}, status=500)
        valid_status = {
            "POST": {201},
            "PUT": {200, 202},
            "PATCH": {200, 202},
            "DELETE": {204, 200},
            "GET": {200},
        }.get(request.method, {200})
        if response.status_code not in valid_status:
            response_data = getattr(response, "data", None)
            logger.error(f"Error {request.method} {request.path}: {response_data}")
        return response


class QuestionViewSet(QuestionExceptionMixin, viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        # Use the mixin's logging/exception handling for dispatch
        return self.handle_request_with_logging_dispatch(
            lambda req, *a, **kw: super(QuestionViewSet, self).dispatch(req, *a, **kw),
            request,
            *args,
            **kwargs,
        )

    def get_queryset(self):  # type: ignore[override]
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionListCreateView(QuestionExceptionMixin, generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        return self.handle_request_with_logging_dispatch(
            lambda req, *a, **kw: super(QuestionListCreateView, self).dispatch(
                req, *a, **kw
            ),
            request,
            *args,
            **kwargs,
        )

    def get_queryset(self):  # type: ignore[override]
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionRetrieveUpdateDestroyView(
    QuestionExceptionMixin, generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        return self.handle_request_with_logging_dispatch(
            lambda req, *a, **kw: super(
                QuestionRetrieveUpdateDestroyView, self
            ).dispatch(req, *a, **kw),
            request,
            *args,
            **kwargs,
        )

    def get_queryset(self):  # type: ignore[override]
        return Question.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
