from django.core.management.base import BaseCommand
from apps.core.models import Tag, Question, QuestionLog
from faker import Faker
import random
from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = "Create fake data for testing purposes"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Tags
        tags = []
        for _ in range(10):
            tag_name = fake.word()
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        # Create Questions
        questions = []
        for _ in range(50):
            question = Question.objects.create(
                title=fake.sentence(),
                source=fake.company(),
                difficulty=random.choice(["Easy", "Medium", "Hard"]),
                description=fake.text(),
                slug=f"{fake.word()}-{fake.uuid4()}",
                is_active=random.choice([True, False]),
                attempts_count=random.randint(1, 5),
                solved_count=random.randint(0, 5),
                last_attempted_at=make_aware(fake.date_time_this_year()),
            )
            question.topic_tags.set(random.sample(tags, random.randint(1, 5)))
            questions.append(question)

        # Create QuestionLogs
        for question in questions:
            for _ in range(random.randint(1, 3)):
                QuestionLog.objects.create(
                    question=question,
                    date_attempted=make_aware(fake.date_time_this_year()),
                    time_spent_min=random.randint(5, 120),
                    outcome=random.choice(["Solved", "Partial", "Failed"]),
                    solution_approach=fake.word(),
                    self_notes=fake.text(),
                )

        self.stdout.write(self.style.SUCCESS("Successfully created fake data"))
