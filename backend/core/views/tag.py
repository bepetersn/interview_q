from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import logging
from ..models import Tag
from ..serializers import TagSerializer

logger = logging.getLogger(__name__)


class TagExceptionMixin:
    def handle_request_with_logging(self, action, request, *args, **kwargs):
        logger.info(f"Entering the {action} method for Tag")
        logger.info(f"Incoming payload: {request.data}")
        try:
            super_method = getattr(super(), action)
            response = super_method(request, *args, **kwargs)
        except ValidationError as exc:
            logger.warning(f"Validation error {action} Tag: {exc}")
            return Response(exc.detail, status=400)
        except Exception as exc:
            logger.error(f"Unexpected error {action} Tag: {exc}")
            return Response({"error": str(exc)}, status=500)
        expected_status = 201 if action == "create" else 200
        if response.status_code != expected_status:
            logger.error(f"Error {action} Tag: {response.data}")
        return response


class TagListCreateView(TagExceptionMixin, generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        tag_name = request.data.get("name")
        if Tag.objects.filter(name=tag_name).exists():
            return Response({"error": "Tag with this name already exists."}, status=400)
        return self.handle_request_with_logging("create", request, *args, **kwargs)


class TagRetrieveUpdateDestroyView(
    TagExceptionMixin, generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore
        return Tag.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        tag_name = request.data.get("name")
        tag_id = self.kwargs.get("pk")
        if (
            Tag.objects.filter(name=tag_name, user=self.request.user)
            .exclude(id=tag_id)
            .exists()
        ):
            return Response({"error": "Tag with this name already exists."}, status=400)
        return super().update(request, *args, **kwargs)
