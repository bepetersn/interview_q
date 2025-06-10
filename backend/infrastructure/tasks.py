import logging
import time
import json
import requests
from django.utils import timezone
from backend.core.models import Question, QuestionLog

logger = logging.getLogger(__name__)


def fetch_codewars_data(username):
    time.sleep(0.1)  # rudimentary rate limiting
    url = f"https://www.codewars.com/api/v1/users/{username}/code-challenges/completed"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logger.error("Codewars fetch failed: %s", exc)
        raise
    data = resp.json()
    results = []
    for item in data.get("data", []):
        results.append({"title": item.get("name"), "difficulty": item.get("rank", {}).get("name", "Easy")})
    return results


def import_questions(platform, username):
    if platform != "codewars":
        raise ValueError(f"Unsupported platform: {platform}")
    try:
        questions = fetch_codewars_data(username)
        for q in questions:
            question, _ = Question.objects.get_or_create(
                title=q["title"], defaults={"difficulty": q.get("difficulty")}
            )
            QuestionLog.objects.create(
                question=question,
                date_attempted=timezone.now(),
                outcome="Solved",
            )
        return {"imported": len(questions)}
    except Exception as exc:
        logger.exception("Import failed")
        raise exc


def handle_sqs_message(message):
    """Dispatches an SQS message to the appropriate task."""
    try:
        payload = json.loads(message)
    except Exception:
        logger.error("Invalid SQS message: %s", message)
        return
    action = payload.get("action")
    data = payload.get("data", {})
    if action == "import_questions":
        import_questions(data.get("platform"), data.get("username"))

