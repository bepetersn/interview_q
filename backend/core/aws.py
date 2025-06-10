import boto3
import logging
import json
import datetime

logger = logging.getLogger(__name__)


def get_sqs_client(region_name=None):
    """
    Returns a boto3 SQS client. Use this directly to publish messages to SQS.
    Example:
        sqs = get_sqs_client()
        sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    """
    return boto3.client("sqs", region_name=region_name or "us-east-1")


def publish_sqs_message(queue_url, action, data, region_name=None, request_meta=None):
    """
    Publishes a message to the specified SQS queue. The message body will include:
      - action: a string describing the background action for Lambda
      - data: the payload for the action
      - request_meta: optional dict of metadata (e.g., user, request id, timestamp)
    """
    sqs = get_sqs_client(region_name=region_name)
    message = {
        "action": action,
        "data": data,
        "meta": request_meta or {},
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }
    return sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
