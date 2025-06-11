from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import logging
from ..models import Tag
from ..serializers import TagSerializer

logger = logging.getLogger(__name__)


class TagListCreateView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.info("Entering the create method for Tag")
        logger.debug(f"Incoming payload: {request.data}")
        try:
            tag_name = request.data.get("name")
            if Tag.objects.filter(name=tag_name).exists():
                return Response(
                    {"error": "Tag with this name already exists."}, status=400
                )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = super().create(request, *args, **kwargs)
            logger.debug(f"Response object: {response}")
        except ValidationError as exc:
            logger.warning(f"Validation error creating Tag: {exc}")
            return Response(exc.detail, status=400)
        except Exception as exc:
            logger.error(f"Unexpected error creating Tag: {exc}")
            return Response({"error": str(exc)}, status=500)
        if response.status_code != 201:
            logger.error(f"Error creating Tag: {response.data}")
        return response


class TagRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)
