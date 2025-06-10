from rest_framework import generics, viewsets
from rest_framework.response import Response
from ..models import Question
from ..serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
