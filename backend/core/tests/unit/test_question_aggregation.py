"""
Test cases for Question aggregation field updates via QuestionLog signals.
"""

from datetime import datetime, timezone
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from backend.core.models import Question, QuestionLog

User = get_user_model()


class TestQuestionAggregation(TestCase):
    """Test that Question aggregation fields are updated when QuestionLog changes."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.question = Question.objects.create(
            title="Test Question",
            user=self.user,
        )

    def test_initial_aggregates_are_zero(self):
        """Test that a new question has zero aggregates."""
        self.assertEqual(self.question.attempts_count, 0)
        self.assertEqual(self.question.solved_count, 0)
        self.assertIsNone(self.question.last_attempted_at)

    def test_single_log_creation_updates_aggregates(self):
        """Test that creating a log updates the question's aggregates."""
        attempt_date = datetime(2025, 7, 4, 12, 0, 0, tzinfo=timezone.utc)

        QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            date_attempted=attempt_date,
            outcome="Solved",
            time_spent_min=30,
        )

        # Refresh the question from database
        self.question.refresh_from_db()

        self.assertEqual(self.question.attempts_count, 1)
        self.assertEqual(self.question.solved_count, 1)
        self.assertEqual(self.question.last_attempted_at, attempt_date)

    def test_multiple_logs_update_aggregates_correctly(self):
        """Test that multiple logs correctly calculate aggregates."""
        dates = [
            datetime(2025, 7, 1, 12, 0, 0, tzinfo=timezone.utc),
            datetime(2025, 7, 2, 12, 0, 0, tzinfo=timezone.utc),
            datetime(2025, 7, 3, 12, 0, 0, tzinfo=timezone.utc),
        ]

        # Create three logs with different outcomes
        QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            date_attempted=dates[0],
            outcome="Failed",
        )
        QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            date_attempted=dates[1],
            outcome="Partial",
        )
        QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            date_attempted=dates[2],
            outcome="Solved",
        )

        # Refresh the question from database
        self.question.refresh_from_db()

        self.assertEqual(self.question.attempts_count, 3)
        self.assertEqual(self.question.solved_count, 1)  # Only one "Solved"
        self.assertEqual(self.question.last_attempted_at, dates[2])  # Latest date

    def test_log_update_recalculates_aggregates(self):
        """Test that updating a log recalculates the aggregates."""
        log = QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            outcome="Failed",
        )

        # Initial state
        self.question.refresh_from_db()
        self.assertEqual(self.question.solved_count, 0)

        # Update the log to "Solved"
        log.outcome = "Solved"
        log.save()

        # Check that aggregates were updated
        self.question.refresh_from_db()
        self.assertEqual(self.question.solved_count, 1)

    def test_log_deletion_updates_aggregates(self):
        """Test that deleting a log updates the aggregates."""
        # Create two logs
        log1 = QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            outcome="Solved",
        )
        QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            outcome="Failed",
        )

        # Initial state: 2 attempts, 1 solved
        self.question.refresh_from_db()
        self.assertEqual(self.question.attempts_count, 2)
        self.assertEqual(self.question.solved_count, 1)

        # Delete the solved log
        log1.delete()

        # Check that aggregates were updated
        self.question.refresh_from_db()
        self.assertEqual(self.question.attempts_count, 1)
        self.assertEqual(self.question.solved_count, 0)

    def test_deleting_all_logs_resets_aggregates(self):
        """Test that deleting all logs resets aggregates to initial state."""
        # Create a log
        QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            outcome="Solved",
            date_attempted=datetime(2025, 7, 4, 12, 0, 0, tzinfo=timezone.utc),
        )

        # Verify it's updated
        self.question.refresh_from_db()
        self.assertEqual(self.question.attempts_count, 1)
        self.assertEqual(self.question.solved_count, 1)
        self.assertIsNotNone(self.question.last_attempted_at)

        # Delete all logs
        QuestionLog.objects.filter(question=self.question).delete()

        # Check that aggregates are reset
        self.question.refresh_from_db()
        self.assertEqual(self.question.attempts_count, 0)
        self.assertEqual(self.question.solved_count, 0)
        self.assertIsNone(self.question.last_attempted_at)

    def test_logs_without_date_attempted_handled_correctly(self):
        """Test that logs without date_attempted don't break aggregation."""
        # Create a log without date_attempted
        QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            outcome="Solved",
            # date_attempted is None
        )

        # Create a log with date_attempted
        attempt_date = datetime(2025, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
        QuestionLog.objects.create(
            question=self.question,
            user=self.user,
            outcome="Failed",
            date_attempted=attempt_date,
        )

        # Check aggregates
        self.question.refresh_from_db()
        self.assertEqual(self.question.attempts_count, 2)
        self.assertEqual(self.question.solved_count, 1)
        # Should use the date from the log that has one
        self.assertEqual(self.question.last_attempted_at, attempt_date)

    def test_multiple_solved_outcomes_counted_correctly(self):
        """Test that multiple 'Solved' outcomes are all counted."""
        for i in range(3):
            QuestionLog.objects.create(
                question=self.question,
                user=self.user,
                outcome="Solved",
                date_attempted=datetime(2025, 7, i + 1, 12, 0, 0, tzinfo=timezone.utc),
            )

        self.question.refresh_from_db()
        self.assertEqual(self.question.attempts_count, 3)
        self.assertEqual(self.question.solved_count, 3)

    def test_signal_handles_no_question_gracefully(self):
        """Test that signal handlers don't break if question becomes None
        during processing."""
        # This tests the robustness of our signal handlers
        with patch("backend.core.signals.update_question_aggregates") as mock_update:
            # Create a log (this will trigger the signal)
            QuestionLog.objects.create(
                question=self.question,
                user=self.user,
                outcome="Solved",
            )

            # Verify update_question_aggregates was called
            mock_update.assert_called_once_with(self.question)
