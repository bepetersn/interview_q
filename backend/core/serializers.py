from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Question, QuestionLog, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "user"]
        read_only_fields = ["user"]


class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source="tags",
    )

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = [
            "user",
            "slug",
        ]  # Mark slug as read-only so it's not required in input

    def to_internal_value(self, data):
        data = data.copy()
        if "slug" in data:
            raise ValidationError(
                {"slug": "Supplying a slug is not allowed. It will be auto-generated."}
            )
        return super().to_internal_value(data)


class QuestionLogSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    title = serializers.ReadOnlyField(source="question.title")

    class Meta:
        model = QuestionLog
        fields = [
            "id",
            "user",
            "question",
            "title",
            "date_attempted",
            "time_spent_min",
            "outcome",
            "solution_approach",
            "self_notes",
        ]
        read_only_fields = ["user"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password")

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs.get("username"), password=attrs.get("password")
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs["user"] = user
        return attrs
