"""
Signal handlers for the core app.

This module contains Django signal handlers that automatically update
Question aggregation fields when QuestionLog instances are created,
updated, or deleted.
"""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import QuestionLog


def update_question_aggregates(question):
    """
    Update the aggregation fields for a question based on its logs.

    Args:
        question: The Question instance to update
    """
    from .models import Question

    logs = question.logs.all()

    # Calculate aggregates
    attempts_count = logs.count()
    solved_count = logs.filter(outcome="Solved").count()

    # Get the most recent attempt date
    latest_log = logs.order_by("-date_attempted").first()
    last_attempted_at = (
        latest_log.date_attempted if latest_log and latest_log.date_attempted else None
    )

    # Update the question with new aggregates
    Question.objects.filter(pk=question.pk).update(
        attempts_count=attempts_count,
        solved_count=solved_count,
        last_attempted_at=last_attempted_at,
    )


@receiver(post_save, sender=QuestionLog)
def update_question_on_log_save(sender, instance, created, **kwargs):
    """
    Update question aggregates when a QuestionLog is created or updated.

    Args:
        sender: The model class (QuestionLog)
        instance: The QuestionLog instance
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    if instance.question:
        update_question_aggregates(instance.question)


@receiver(post_delete, sender=QuestionLog)
def update_question_on_log_delete(sender, instance, **kwargs):
    """
    Update question aggregates when a QuestionLog is deleted.

    Args:
        sender: The model class (QuestionLog)
        instance: The QuestionLog instance being deleted
        **kwargs: Additional keyword arguments
    """
    if instance.question:
        update_question_aggregates(instance.question)
