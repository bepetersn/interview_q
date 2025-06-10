from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import logging
from ..models import QuestionLog
from ..serializers import QuestionLogSerializer

logger = logging.getLogger(__name__)


class QuestionLogViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuestionLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionLogListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuestionLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.info("Entering the create method")
        logger.debug(f"Incoming payload: {request.data}")
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = super().create(request, *args, **kwargs)
        except ValidationError as exc:
            logger.warning(f"Validation error creating QuestionLog: {exc}")
            logger.warning(f"Validation error creating QuestionLog: {exc}")
            return Response(exc.detail, status=400)
        except Exception as exc:
            logger.error(f"Unexpected error creating QuestionLog: {exc}")
            return Response({"error": str(exc)}, status=500)
        if response.status_code != 201:
            logger.error(f"Error creating QuestionLog: {response.data}")
        return response


class QuestionLogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuestionLog.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        logger.info("Entering the update method for QuestionLog")
        logger.debug(f"Incoming payload: {request.data}")
        try:
            try:
                self.get_object()
            except Exception as exc:
                logger.warning(f"Object not found for update: {exc}")
                return Response({"detail": "Not found."}, status=404)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = super().update(request, *args, **kwargs)
            logger.debug(f"Response object: {response}")
        except ValidationError as exc:
            logger.warning(f"Validation error updating QuestionLog: {exc}")
            return Response(exc.detail, status=400)
        except Exception as exc:
            logger.error(f"Unexpected error updating QuestionLog: {exc}")
            return Response({"error": str(exc)}, status=500)
        if response.status_code != 200:
            logger.error(f"Error updating QuestionLog: {response.data}")
        return response
