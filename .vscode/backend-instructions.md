# Backend Development Instructions

## Django/DRF Standards

### Model Best Practices
```python
from django.db import models
from django.core.validators import MinLengthValidator

class Question(models.Model):
    """Model representing an interview question."""

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(5)],
        help_text="Brief descriptive title"
    )
    content = models.TextField(help_text="Full question content")
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['difficulty', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})
```

### ViewSet Best Practices
```python
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing interview questions."""

    queryset = Question.objects.select_related('category').prefetch_related('tags')
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['difficulty', 'is_active']
    search_fields = ['title', 'content']

    def get_queryset(self):
        """Optimize queries and apply user-specific filtering."""
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            # Apply user-specific filtering
            pass

        return queryset

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark a question as completed by the user."""
        question = self.get_object()
        # Implementation here
        return Response({'status': 'completed'})
```

### Serializer Best Practices
```python
from rest_framework import serializers
from .models import Question, Tag

class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model."""

    tags = serializers.StringRelatedField(many=True, read_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False
    )

    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'difficulty', 'tags', 'tag_names', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """Validate question title."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value.strip()

    def create(self, validated_data):
        """Create question with tags."""
        tag_names = validated_data.pop('tag_names', [])
        question = Question.objects.create(**validated_data)

        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            question.tags.add(tag)

        return question
```

## Testing Standards

### Model Tests
```python
import pytest
from django.core.exceptions import ValidationError
from backend.core.models import Question

@pytest.mark.django_db
class TestQuestionModel:
    """Test cases for Question model."""

    def test_create_question(self):
        """Test creating a valid question."""
        question = Question.objects.create(
            title="Test Question",
            content="What is the time complexity?",
            difficulty="medium"
        )
        assert question.title == "Test Question"
        assert question.is_active is True

    def test_question_str_representation(self):
        """Test string representation of question."""
        question = Question(title="Test Question")
        assert str(question) == "Test Question"

    def test_invalid_title_length(self):
        """Test validation for title length."""
        with pytest.raises(ValidationError):
            question = Question(title="Hi", content="Test")
            question.full_clean()
```

### ViewSet Tests
```python
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestQuestionViewSet:
    """Test cases for Question ViewSet."""

    def test_list_questions(self, api_client, sample_questions):
        """Test listing questions."""
        url = reverse('question-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(sample_questions)

    def test_create_question(self, api_client, authenticated_user):
        """Test creating a new question."""
        url = reverse('question-list')
        data = {
            'title': 'New Question',
            'content': 'Question content here',
            'difficulty': 'easy'
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Question'

    def test_unauthorized_access(self, api_client):
        """Test unauthorized access to protected endpoints."""
        url = reverse('question-list')
        response = api_client.post(url, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

## Common Patterns

### Error Handling
```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error responses."""
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data
        }
        response.data = custom_response_data

    return response
```

### Custom Managers
```python
class ActiveQuestionManager(models.Manager):
    """Manager for active questions only."""

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def by_difficulty(self, difficulty):
        return self.get_queryset().filter(difficulty=difficulty)
```

### Utility Functions
```python
from django.core.cache import cache
from typing import List, Optional

def get_or_set_cache(key: str, func, timeout: int = 300) -> any:
    """Get value from cache or set it using provided function."""
    value = cache.get(key)
    if value is None:
        value = func()
        cache.set(key, value, timeout)
    return value

def bulk_create_with_tags(questions_data: List[dict]) -> List[Question]:
    """Bulk create questions with associated tags."""
    questions = []
    for data in questions_data:
        tag_names = data.pop('tags', [])
        question = Question(**data)
        questions.append(question)

    created_questions = Question.objects.bulk_create(questions)
    # Handle tags separately for bulk operations
    return created_questions
```

## Performance Optimization

### Database Queries
- Use select_related() for ForeignKey relationships
- Use prefetch_related() for ManyToMany relationships
- Add database indexes for commonly queried fields
- Use bulk operations for multiple records
- Implement pagination for large datasets

### Caching
- Cache expensive queries
- Use Memcached for session storage
- Implement cache invalidation strategies
- Cache serialized data when appropriate

## Security Best Practices

### Input Validation
- Validate all user inputs
- Use Django's built-in validators
- Implement custom validators for business logic
- Sanitize data before database operations

### Authentication & Authorization
- Use Django's built-in authentication
- Implement proper permission classes
- Use JWT tokens for API authentication
- Validate user permissions at the view level

### API Security
- Implement rate limiting
- Use CORS properly
- Validate request origins
- Log security events
