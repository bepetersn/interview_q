"""
Integration tests for Question aggregation functionality.

These tests verify that the Question model's aggregation fields
(attempts_count, solved_count, last_attempted_at) are properly
updated via signals when QuestionLog instances are manipulated
through the Django ORM.
"""

from datetime import datetime, timezone

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from backend.core.models import Question, QuestionLog

User = get_user_model()


@pytest.mark.django_db
class TestQuestionAggregationIntegration(TestCase):
    """Integration tests for Question aggregation via signals."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="integrationuser", password="testpass"
        )

    def test_end_to_end_aggregation_workflow(self):
        """
        Test a complete workflow of question log creation, updates, and deletion
        to verify that aggregation fields are maintained correctly via signals.
        """
        # Create a question
        question = Question.objects.create(
            title="Integration Test Question",
            user=self.user,
            content="Test question for integration testing",
            difficulty="Medium",
        )

        # Verify initial state
        self.assertEqual(question.attempts_count, 0)
        self.assertEqual(question.solved_count, 0)
        self.assertIsNone(question.last_attempted_at)
        print(
            f"Initial state: attempts={question.attempts_count}, "
            f"solved={question.solved_count}, "
            f"last_attempted={question.last_attempted_at}"
        )

        # Step 1: Create first attempt (Failed)
        attempt_date_1 = datetime(2025, 7, 1, 12, 0, 0, tzinfo=timezone.utc)
        log1 = QuestionLog.objects.create(
            question=question,
            user=self.user,
            date_attempted=attempt_date_1,
            outcome="Failed",
            time_spent_min=45,
            solution_approach="Brute force",
            self_notes="Need to optimize",
        )

        question.refresh_from_db()
        self.assertEqual(question.attempts_count, 1)
        self.assertEqual(question.solved_count, 0)
        self.assertEqual(question.last_attempted_at, attempt_date_1)
        print(
            f"After 1 failed attempt: attempts={question.attempts_count}, "
            f"solved={question.solved_count}, "
            f"last_attempted={question.last_attempted_at}"
        )

        # Step 2: Create second attempt (Partial)
        attempt_date_2 = datetime(2025, 7, 2, 14, 30, 0, tzinfo=timezone.utc)
        log2 = QuestionLog.objects.create(
            question=question,
            user=self.user,
            date_attempted=attempt_date_2,
            outcome="Partial",
            time_spent_min=60,
            solution_approach="Dynamic programming",
            self_notes="Getting closer",
        )

        question.refresh_from_db()
        self.assertEqual(question.attempts_count, 2)
        self.assertEqual(question.solved_count, 0)
        self.assertEqual(question.last_attempted_at, attempt_date_2)
        print(
            f"After 2 attempts (1 partial): attempts={question.attempts_count}, "
            f"solved={question.solved_count}, "
            f"last_attempted={question.last_attempted_at}"
        )

        # Step 3: Create third attempt (Solved)
        attempt_date_3 = datetime(2025, 7, 3, 10, 15, 0, tzinfo=timezone.utc)
        log3 = QuestionLog.objects.create(
            question=question,
            user=self.user,
            date_attempted=attempt_date_3,
            outcome="Solved",
            time_spent_min=30,
            solution_approach="Optimized DP",
            self_notes="Finally got it!",
        )

        question.refresh_from_db()
        self.assertEqual(question.attempts_count, 3)
        self.assertEqual(question.solved_count, 1)
        self.assertEqual(question.last_attempted_at, attempt_date_3)
        print(
            f"After 3 attempts (1 solved): attempts={question.attempts_count}, "
            f"solved={question.solved_count}, "
            f"last_attempted={question.last_attempted_at}"
        )

        # Step 4: Update first log to be "Solved" as well
        log1.outcome = "Solved"
        log1.self_notes = "Actually, this was correct too"
        log1.save()

        question.refresh_from_db()
        self.assertEqual(question.attempts_count, 3)
        self.assertEqual(question.solved_count, 2)  # Now 2 solved
        self.assertEqual(
            question.last_attempted_at, attempt_date_3
        )  # Still latest date
        print(
            f"After updating log1 to solved: attempts={question.attempts_count}, "
            f"solved={question.solved_count}, "
            f"last_attempted={question.last_attempted_at}"
        )

        # Step 5: Delete the partial attempt (log2)
        log2.delete()

        question.refresh_from_db()
        self.assertEqual(question.attempts_count, 2)
        self.assertEqual(question.solved_count, 2)  # Both remaining are solved
        self.assertEqual(
            question.last_attempted_at, attempt_date_3
        )  # Still latest date
        print(
            f"After deleting log2: attempts={question.attempts_count}, "
            f"solved={question.solved_count}, "
            f"last_attempted={question.last_attempted_at}"
        )

        # Step 6: Delete the latest attempt (log3)
        log3.delete()

        question.refresh_from_db()
        self.assertEqual(question.attempts_count, 1)
        self.assertEqual(question.solved_count, 1)
        self.assertEqual(
            question.last_attempted_at, attempt_date_1
        )  # Now earliest is latest
        print(
            f"After deleting log3: attempts={question.attempts_count}, "
            f"solved={question.solved_count}, "
            f"last_attempted={question.last_attempted_at}"
        )

        # Step 7: Delete all remaining logs
        log1.delete()

        question.refresh_from_db()
        self.assertEqual(question.attempts_count, 0)
        self.assertEqual(question.solved_count, 0)
        self.assertIsNone(question.last_attempted_at)
        print(
            f"After deleting all logs: attempts={question.attempts_count}, "
            f"solved={question.solved_count}, "
            f"last_attempted={question.last_attempted_at}"
        )

        print("Integration test completed successfully!")

    def test_multiple_individual_operations_update_aggregates(self):
        """Test that multiple individual log operations correctly update aggregates.

        This test reflects real application usage where logs are created/deleted
        individually through the API, not in bulk operations.
        """
        question = Question.objects.create(
            title="Multiple Operations Test Question", user=self.user
        )

        # Create multiple logs individually (as the real app does)
        for i in range(5):
            QuestionLog.objects.create(
                question=question,
                user=self.user,
                date_attempted=datetime(2025, 7, i + 1, 12, 0, 0, tzinfo=timezone.utc),
                outcome="Solved" if i % 2 == 0 else "Failed",  # Alternate outcomes
                time_spent_min=30 + i * 10,
            )

        question.refresh_from_db()
        self.assertEqual(question.attempts_count, 5)
        self.assertEqual(question.solved_count, 3)  # indexes 0, 2, 4 are "Solved"
        self.assertEqual(
            question.last_attempted_at,
            datetime(2025, 7, 5, 12, 0, 0, tzinfo=timezone.utc),  # Latest date
        )

        # Individual delete operations (as the real app does)
        failed_logs = QuestionLog.objects.filter(question=question, outcome="Failed")
        for log in failed_logs:
            log.delete()

        question.refresh_from_db()
        self.assertEqual(question.attempts_count, 3)  # Only "Solved" logs remain
        self.assertEqual(question.solved_count, 3)

    def test_multiple_questions_independence(self):
        """Test that aggregation updates for one question don't affect others."""
        question1 = Question.objects.create(title="Question 1", user=self.user)
        question2 = Question.objects.create(title="Question 2", user=self.user)

        # Add logs to question1
        QuestionLog.objects.create(
            question=question1,
            user=self.user,
            outcome="Solved",
            date_attempted=datetime(2025, 7, 1, 12, 0, 0, tzinfo=timezone.utc),
        )

        # Add logs to question2
        QuestionLog.objects.create(
            question=question2,
            user=self.user,
            outcome="Failed",
            date_attempted=datetime(2025, 7, 2, 12, 0, 0, tzinfo=timezone.utc),
        )

        # Refresh both questions
        question1.refresh_from_db()
        question2.refresh_from_db()

        # Verify each question has correct aggregates
        self.assertEqual(question1.attempts_count, 1)
        self.assertEqual(question1.solved_count, 1)

        self.assertEqual(question2.attempts_count, 1)
        self.assertEqual(question2.solved_count, 0)

        # Verify dates are different
        self.assertEqual(
            question1.last_attempted_at,
            datetime(2025, 7, 1, 12, 0, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            question2.last_attempted_at,
            datetime(2025, 7, 2, 12, 0, 0, tzinfo=timezone.utc),
        )

    def test_signal_performance_with_many_logs(self):
        """Test that signals perform reasonably well with many logs."""
        question = Question.objects.create(title="Performance Test", user=self.user)

        # Create many logs
        num_logs = 50
        for i in range(num_logs):
            QuestionLog.objects.create(
                question=question,
                user=self.user,
                outcome="Solved" if i % 3 == 0 else "Failed",
                date_attempted=datetime(2025, 7, 1, 12, i, 0, tzinfo=timezone.utc),
            )

        question.refresh_from_db()
        expected_solved = len([i for i in range(num_logs) if i % 3 == 0])

        self.assertEqual(question.attempts_count, num_logs)
        self.assertEqual(question.solved_count, expected_solved)
        self.assertEqual(
            question.last_attempted_at,
            datetime(2025, 7, 1, 12, num_logs - 1, 0, tzinfo=timezone.utc),
        )
