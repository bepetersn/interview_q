# Example Lambda handler for SQS events
# Place your actual logic here


def main(event, context):
    for record in event["Records"]:
        print(f"Received SQS message: {record['body']}")
    return {"statusCode": 200}
