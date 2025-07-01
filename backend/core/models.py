from django.conf import settings
from django.db import models

from .utils import SlugGenerator


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(
        blank=True, help_text="Detailed description of the tag"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the tag was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the tag was last updated"
    )
    is_active = models.BooleanField(
        default=True, help_text="Indicates if the tag is active"
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


class Question(models.Model):

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

    # Time tracking / Status

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the question was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the question was last updated"
    )
    is_active = models.BooleanField(
        default=True, help_text="Indicates if the question is active"
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

    def __init__(self, *args, **kwargs):
        # Remove slug from kwargs to prevent user-supplied slug
        kwargs.pop("slug", None)
        super().__init__(*args, **kwargs)
        self.slug = SlugGenerator.generate_unique_slug(self.__class__, self.title)

    def __str__(self):
        return f"{self.title} [{self.slug}]"


class QuestionLog(models.Model):
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
