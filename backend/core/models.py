from django.conf import settings
from django.db import models

from .utils import SlugGenerator


class BaseModel(models.Model):
    """Base model with common fields and behavior"""

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the record was last updated"
    )
    is_active = models.BooleanField(
        default=True, help_text="Indicates if the record is active"
    )

    class Meta:
        abstract = True


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(
        blank=True, help_text="Detailed description of the tag"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tags",
        null=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Question(BaseModel):
    """Interview question model with automatic slug generation"""

    # Intrinsic / Essential data
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    title = models.CharField(max_length=255)
    source = models.CharField(
        max_length=4095,
        blank=True,
        help_text="e.g., LeetCode, personal interview",
    )
    content = models.TextField(
        blank=True, help_text="Detailed description of the question"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="URL-friendly identifier for the question",
        blank=True,
        editable=False,  # Slug is auto-generated and should not be set by users
    )
    difficulty = models.CharField(
        max_length=6,
        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="questions", help_text="Tags for the question"
    )

    # QuestionLog aggregation data
    attempts_count = models.PositiveIntegerField(default=0)
    solved_count = models.PositiveIntegerField(
        default=0, help_text="Number of times this question has been solved"
    )
    last_attempted_at = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp of the last attempt"
    )

    class Meta:
        ordering = ["-created_at", "title"]

    def save(self, *args, **kwargs):
        """Override save to generate slug before saving"""
        if not self.slug:
            self.slug = SlugGenerator.generate_unique_slug(self.__class__, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} [{self.slug}]"


class QuestionLog(models.Model):
    """Log of attempts on questions"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="question_logs",
        null=True,
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="logs"
    )
    date_attempted = models.DateTimeField(null=True, blank=True)
    time_spent_min = models.PositiveIntegerField(
        null=True, blank=True, help_text="Time spent in minutes"
    )
    outcome = models.CharField(
        max_length=40,
        choices=[("Solved", "Solved"), ("Partial", "Partial"), ("Failed", "Failed")],
        blank=True,
    )
    solution_approach = models.CharField(
        max_length=100, blank=True, help_text="e.g., Brute force, Optimized"
    )
    self_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date_attempted"]
        verbose_name = "Question Log"
        verbose_name_plural = "Question Logs"

    def __str__(self):
        date_str = (
            self.date_attempted.strftime("%Y-%m-%d") if self.date_attempted else "N/A"
        )
        return f"{self.question.title} ({self.outcome}) - {date_str}"
