#!/usr/bin/env python3
import aws_cdk as cdk
from infra.sqs_lambda_stack import ServerlessStack

app = cdk.App()
ServerlessStack(app, "ServerlessStack")
app.synth()
