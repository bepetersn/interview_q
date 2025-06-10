from rest_framework import serializers
from .models import Question, QuestionLog, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionLogSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    title = serializers.ReadOnlyField(source="question.title")

    class Meta:
        model = QuestionLog
        fields = [
            "id",
            "question",
            "title",
            "date_attempted",
            "time_spent_min",
            "outcome",
            "solution_approach",
            "self_notes",
        ]
