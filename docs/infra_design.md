# This directory contains AWS CDK infrastructure for SQS and Lambda integration.
#
# Structure:
# - app.py: CDK entrypoint
# - sqs_lambda_stack.py: Defines SQS queue, DLQ, Lambda, and roles
# - lambda/: Lambda handler code
# - requirements.txt: CDK Python dependencies
#
# To deploy:
# 1. Install dependencies: pip install -r requirements.txt
# 2. Bootstrap your AWS environment: cdk bootstrap
# 3. Deploy: cdk deploy
