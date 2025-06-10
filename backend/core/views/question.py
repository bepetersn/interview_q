from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from ..models import Question
from ..serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
