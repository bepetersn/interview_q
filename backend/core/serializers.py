from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Question, QuestionLog, Tag
from .utils import sanitize_html


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class QuestionSerializer(serializers.ModelSerializer):
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True,
    )
    tags = TagSerializer(many=True, read_only=True)
    last_attempted_at = serializers.DateTimeField(read_only=True)
    attempts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "content",
            "difficulty",
            "source",
            "is_active",
            "tag_ids",
            "slug",
            "tags",
            "title",
            "created_at",
            "updated_at",
            "last_attempted_at",
            "attempts_count",
        ]
        read_only_fields = [
            "id",
            "user",
            "slug",
            "created_at",
            "updated_at",
            "last_attempted_at",
            "attempts_count",
        ]

    def validate_tag_ids(self, value):
        """Validate that all tag_ids belong to the current user"""
        if not value:
            return value

        request = self.context.get("request")
        if (
            not request
            or not hasattr(request, "user")
            or not request.user.is_authenticated
        ):
            raise serializers.ValidationError("Authentication required")

        # Check that all provided tag IDs exist and belong to the user
        user_tag_ids = set(
            Tag.objects.filter(user=request.user).values_list("id", flat=True)
        )
        provided_tag_ids = set(value)

        invalid_tag_ids = provided_tag_ids - user_tag_ids
        if invalid_tag_ids:
            raise serializers.ValidationError(f"Invalid tag IDs: {invalid_tag_ids}")

        return value

    def validate_title(self, value):
        """Ensure that the title is always present and not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title is required and cannot be empty.")
        return value

    def to_internal_value(self, data):
        data = data.copy()
        if "slug" in data:
            raise ValidationError(
                {"slug": "Supplying a slug is not allowed. It will be auto-generated."}
            )
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        # Handle tag_ids separately if provided
        tag_ids = validated_data.pop("tag_ids", None)

        # Update other fields
        instance = super().update(instance, validated_data)

        # Update tags if tag_ids were provided
        if tag_ids is not None:
            tags = Tag.objects.filter(id__in=tag_ids, user=instance.user)
            instance.tags.set(tags)

        return instance

    def create(self, validated_data):
        # Handle tag_ids separately during creation
        tag_ids = validated_data.pop("tag_ids", [])

        # Create the instance
        instance = super().create(validated_data)

        # Set tags if tag_ids were provided
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids, user=instance.user)
            instance.tags.set(tags)

        return instance

    def validate_content(self, value):
        """
        Sanitize the content field to prevent XSS attacks and clean excessive newlines.
        """
        return sanitize_html(value)


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
