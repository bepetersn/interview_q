from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import logging
from .models import QuestionLog, Tag, Question
from .serializers import QuestionLogSerializer, TagSerializer, QuestionSerializer

logger = logging.getLogger(__name__)


class QuestionLogListCreateView(generics.ListCreateAPIView):
    queryset = QuestionLog.objects.all()
    serializer_class = QuestionLogSerializer

    def create(self, request, *args, **kwargs):
        logger.info("Entering the create method")
        logger.debug(f"Incoming payload: {request.data}")
        try:
            # Validate payload
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
    queryset = QuestionLog.objects.all()
    serializer_class = QuestionLogSerializer

    def update(self, request, *args, **kwargs):
        logger.info("Entering the update method for QuestionLog")
        logger.debug(f"Incoming payload: {request.data}")
        import pdb; pdb.set_trace()
        try:
            # Check if the instance exists, return 404 if not
            try:
                self.get_object()
            except Exception as exc:
                logger.warning(f"Object not found for update: {exc}")
                return Response({"detail": "Not found."}, status=404)
            # Validate payload
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


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def create(self, request, *args, **kwargs):
        logger.info("Entering the create method for Tag")
        logger.debug(f"Incoming payload: {request.data}")
        try:
            # Check for existing tag
            tag_name = request.data.get("name")
            if Tag.objects.filter(name=tag_name).exists():
                return Response(
                    {"error": "Tag with this name already exists."}, status=400
                )

            # Validate payload
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


class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionLogViewSet(viewsets.ModelViewSet):
    queryset = QuestionLog.objects.all()
    serializer_class = QuestionLogSerializer


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
            except Exception as e:
                # Handle unique constraint errors (e.g., slug)
                return Response({"error": str(e)}, status=400)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
