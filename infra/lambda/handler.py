"""Lambda handler for processing SQS events."""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from backend.infrastructure.tasks import handle_sqs_message


def main(event, context):
    for record in event.get("Records", []):
        handle_sqs_message(record.get("body", ""))
    return {"statusCode": 200}
