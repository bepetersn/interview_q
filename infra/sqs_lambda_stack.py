from aws_cdk import Duration, Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class ServerlessStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Dead Letter Queue
        dlq = sqs.Queue(
            self, "MyDLQ", queue_name="my-app-dlq", retention_period=Duration.days(14)
        )

        # Main SQS Queue
        queue = sqs.Queue(
            self,
            "MyQueue",
            queue_name="my-app-queue",
            visibility_timeout=Duration.seconds(60),
            dead_letter_queue=sqs.DeadLetterQueue(max_receive_count=3, queue=dlq),
        )

        # Lambda Role (basic sketch)
        lambda_role = iam.Role(
            self,
            "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )
        queue.grant_consume_messages(lambda_role)

        # Lambda Function (handler code to be added separately)
        lambda_fn = _lambda.Function(
            self,
            "MyQueueHandler",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.main",
            code=_lambda.Code.from_asset("lambda"),
            role=lambda_role,
            environment={"QUEUE_URL": queue.queue_url},
            timeout=Duration.seconds(60),
        )
        # Add event source mapping
        lambda_fn.add_event_source_mapping(
            "SQSEventSource",
            event_source_arn=queue.queue_arn,
            batch_size=1,
        )
