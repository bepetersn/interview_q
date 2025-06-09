from rest_framework import generics, viewsets
from rest_framework.response import Response
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
            logger.debug(f"Response object: {response}")
        except Exception as e:
            logger.error(f"Exception during create: {e}")
            return Response({"error": str(e)}, status=500)
        if response.status_code != 201:
            logger.error(f"Error creating QuestionLog: {response.data}")
        return response


class QuestionLogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionLog.objects.all()
    serializer_class = QuestionLogSerializer


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
        except Exception as e:
            logger.error(f"Exception during create: {e}")
            return Response({"error": str(e)}, status=500)
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
