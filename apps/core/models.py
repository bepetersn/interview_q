from django.db import models
from django.utils.text import slugify
import hashlib


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(
        null=True, blank=True, help_text="Detailed description of the tag"
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

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):

    # Intrinsic / Essential data

    title = models.CharField(max_length=255)
    source = models.CharField(
        max_length=4095,
        null=True,
        blank=True,
        help_text="e.g., LeetCode, personal interview",
    )
    notes = models.TextField(
        null=True, blank=True, help_text="Detailed description of the question"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="URL-friendly identifier for the question",
    )
    difficulty = models.CharField(
        max_length=6,
        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
        null=True,
        blank=True,
    )
    topic_tags = models.ManyToManyField(
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
        kwargs.pop('slug', None)
        super().__init__(*args, **kwargs)
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            # Add a hash to ensure uniqueness
            hash_suffix = hashlib.sha1(self.title.encode('utf-8')).hexdigest()[:8]
            self.slug = f"{base_slug}-{hash_suffix}"

    def __str__(self):
        return f"{self.title} [{self.slug}]"


class QuestionLog(models.Model):
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
        null=True,
        blank=True,
    )
    solution_approach = models.CharField(
        max_length=100, null=True, blank=True, help_text="e.g., Brute force, Optimized"
    )
    self_notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-date_attempted"]
        verbose_name = "Question Log"
        verbose_name_plural = "Question Logs"

    def __str__(self):
        date_str = (
            self.date_attempted.strftime('%Y-%m-%d')
            if self.date_attempted else 'N/A'
        )
        return f"{self.question.title} ({self.outcome}) - {date_str}"
