import json
import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockService:
    """A wrapper class for interacting with AWS Bedrock service."""

    def __init__(self, region='eu-west-2') -> None:
        """Initialize the Bedrock client."""
        self.region = region or os.environ.get("AWS_REGION", "us-west-2")
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Private method to initialize the AWS Bedrock client."""
        try:
            return boto3.client("bedrock-runtime", region_name=self.region)
        except NoCredentialsError:
            raise RuntimeError(
                "🟥 Invalid AWS credentials. Please configure AWS credentials.")
        except Exception as e:
            raise RuntimeError(
                f"🟥 Failed to initialize AWS Bedrock client. Cause: {e}")

    def invoke_model(self, model_id, payload):
        """Invoke a Bedrock model with the given payload.

        Args:
            model_id (str): The ID of the model to invoke.
            payload (dict): The request payload.

        Returns:
            dict: The response from the model invocation.

        Raises:
            RuntimeError: If the invocation fails.
        """
        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(payload),
            )
            response_body = response["body"].read().decode("utf-8")
            return json.loads(response_body)
        except ClientError as e:
            raise RuntimeError(
                f"🟥 Failed to invoke model {model_id}. AWS error: {e}")
        except Exception as e:
            raise RuntimeError(
                f"🟥 Unexpected error during model invocation: {e}")
