from typing import Any, Dict, List, Optional

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Question, QuestionLog, Tag
from .utils import sanitize_html


class BaseValidationMixin:
    """Base mixin for common validation patterns"""

    def validate_required_field(self, value: Any, field_name: str) -> Any:
        """Validate that a required field is not empty"""
        if not value or (isinstance(value, str) and not value.strip()):
            raise serializers.ValidationError(
                f"{field_name} is required and cannot be empty."
            )
        return value


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""

    class Meta:
        model = Tag
        fields = ["id", "name"]


class QuestionSerializer(BaseValidationMixin, serializers.ModelSerializer):
    """Serializer for Question model with comprehensive validation"""

    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True,
        help_text="List of tag IDs to associate with this question",
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

    def validate_tag_ids(self, value: List[int]) -> List[int]:
        """Validate that all tag_ids belong to the current user"""
        if not value:
            return value

        user = self._get_current_user()
        if not user:
            raise serializers.ValidationError("Authentication required")

        # Get valid tag IDs for this user
        valid_tag_ids = set(Tag.objects.filter(user=user).values_list("id", flat=True))
        provided_tag_ids = set(value)

        # Check for invalid tag IDs
        invalid_tag_ids = provided_tag_ids - valid_tag_ids
        if invalid_tag_ids:
            raise serializers.ValidationError(
                f"Invalid tag IDs: {sorted(invalid_tag_ids)}"
            )

        return value

    def validate_title(self, value: str) -> str:
        """Validate that the title is present and not empty"""
        return self.validate_required_field(value, "Title")

    def validate_content(self, value: Optional[str]) -> Optional[str]:
        """Sanitize the content field to prevent XSS attacks"""
        return sanitize_html(value) if value else value

    def validate_difficulty(self, value: str) -> str:
        """Validate difficulty choice"""
        if value and value not in ["Easy", "Medium", "Hard"]:
            raise serializers.ValidationError(
                "Difficulty must be Easy, Medium, or Hard"
            )
        return value

    def to_internal_value(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Override to prevent user-supplied slug and ensure proper validation"""
        data = data.copy()

        # Remove slug if provided - it will be auto-generated
        if "slug" in data:
            raise ValidationError(
                {"slug": "Supplying a slug is not allowed. It will be auto-generated."}
            )

        return super().to_internal_value(data)

    def _get_current_user(self):
        """Get the current user from the request context"""
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            return request.user
        return None

    def _update_tags(self, instance: Question, tag_ids: Optional[List[int]]) -> None:
        """Update tags for a question instance"""
        if tag_ids is not None:
            tags = Tag.objects.filter(id__in=tag_ids, user=instance.user)
            instance.tags.set(tags)

    def update(self, instance: Question, validated_data: Dict[str, Any]) -> Question:
        """Update a question instance"""
        tag_ids = validated_data.pop("tag_ids", None)

        # Update other fields
        instance = super().update(instance, validated_data)

        # Update tags if provided
        self._update_tags(instance, tag_ids)

        return instance

    def create(self, validated_data: Dict[str, Any]) -> Question:
        """Create a new question instance"""
        tag_ids = validated_data.pop("tag_ids", [])

        # Create the instance
        instance = super().create(validated_data)

        # Set tags if provided
        self._update_tags(instance, tag_ids)

        return instance


class QuestionLogSerializer(serializers.ModelSerializer):
    """Serializer for QuestionLog model"""

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

    def validate_outcome(self, value: str) -> str:
        """Validate outcome choice"""
        if value and value not in ["Solved", "Partial", "Failed"]:
            raise serializers.ValidationError(
                "Outcome must be Solved, Partial, or Failed"
            )
        return value

    def validate_time_spent_min(self, value: Optional[int]) -> Optional[int]:
        """Validate time spent is positive"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Time spent must be positive")
        return value


class AuthSerializerMixin:
    """Mixin for authentication-related serializers"""

    def validate_username(self, value: str) -> str:
        """Validate username format"""
        if not value or not value.strip():
            raise serializers.ValidationError("Username is required")

        # Add username format validation if needed
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long"
            )

        return value.strip()

    def validate_password(self, value: str) -> str:
        """Validate password strength"""
        if not value:
            raise serializers.ValidationError("Password is required")

        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )

        return value


class RegisterSerializer(AuthSerializerMixin, serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password")

    def create(self, validated_data: Dict[str, Any]):
        """Create a new user"""
        return get_user_model().objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )


class LoginSerializer(AuthSerializerMixin, serializers.Serializer):
    """Serializer for user login"""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate login credentials"""
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("Username and password are required")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        attrs["user"] = user
        return attrs
