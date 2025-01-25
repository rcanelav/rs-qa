import json
import pytest
from unittest.mock import patch, MagicMock
from src.bedrock_service import BedrockService
from botocore.exceptions import NoCredentialsError, ClientError


class TestBedrockService:
    """Unit tests for the BedrockService class."""
    region = "us-west-2"

    @pytest.fixture
    def mock_boto3_client(self):
        """Fixture to mock boto3 client."""
        with patch("src.bedrock_service.boto3.client") as mock_client:
            yield mock_client

    def test_initialize_client_success(self, mock_boto3_client):
        """Test successful initialization of the BedrockService client."""
        # Arrange
        mock_boto3_client.return_value = MagicMock()

        # Act
        service = BedrockService(region=self.region)

        # Assert
        mock_boto3_client.assert_called_once_with("bedrock-runtime", region_name=self.region)
        assert service.client is not None

    def test_initialize_client_no_credentials(self, mock_boto3_client):
        """Test initialization failure due to missing credentials."""
        # Arrange
        mock_boto3_client.side_effect = NoCredentialsError

        # Act & Assert
        with pytest.raises(RuntimeError, match="🟥 Invalid AWS credentials."):
            BedrockService(region=self.region)

    def test_initialize_client_generic_error(self, mock_boto3_client):
        """Test initialization failure due to a generic exception."""
        # Arrange
        mock_boto3_client.side_effect = Exception("Mocked initialization error")

        # Act & Assert
        with pytest.raises(RuntimeError, match="🟥 Failed to initialize AWS Bedrock client. Cause: Mocked initialization error"):
            BedrockService(region=self.region)

    def test_invoke_model_success(self, mock_boto3_client):
        """Test successful invocation of a Bedrock model."""
        # Arrange
        mock_boto3_client.return_value = MagicMock()
        mock_client_instance = mock_boto3_client.return_value
        mock_client_instance.invoke_model.return_value = {
            "body": MagicMock(read=lambda: b'{"content": [{"text": "Mocked response"}]}')
        }

        service = BedrockService(region=self.region)
        model_id = "mock-model-id"
        payload = {"key": "value"}

        # Act
        response = service.invoke_model(model_id=model_id, payload=payload)

        # Assert
        mock_client_instance.invoke_model.assert_called_once_with(
            modelId=model_id,
            body=json.dumps(payload),
        )
        assert response == {"content": [{"text": "Mocked response"}]}

    def test_invoke_model_client_error(self, mock_boto3_client):
        """Test invocation failure due to an AWS ClientError."""
        # Arrange
        mock_boto3_client.return_value = MagicMock()
        mock_client_instance = mock_boto3_client.return_value
        mock_client_instance.invoke_model.side_effect = ClientError(
            error_response={"Error": {"Code": "MockError", "Message": "Mocked AWS ClientError"}},
            operation_name="InvokeModel"
        )

        service = BedrockService(region=self.region)
        model_id = "mock-model-id"
        payload = {"key": "value"}

        # Act & Assert
        with pytest.raises(RuntimeError, match="🟥 Failed to invoke model mock-model-id. AWS error:"):
            service.invoke_model(model_id=model_id, payload=payload)

    def test_invoke_model_generic_error(self, mock_boto3_client):
        """Test invocation failure due to a generic exception."""
        # Arrange
        mock_boto3_client.return_value = MagicMock()
        mock_client_instance = mock_boto3_client.return_value
        mock_client_instance.invoke_model.side_effect = Exception("Mocked invocation error")

        service = BedrockService(region=self.region)
        model_id = "mock-model-id"
        payload = {"key": "value"}

        # Act & Assert
        with pytest.raises(RuntimeError, match="🟥 Unexpected error during model invocation: Mocked invocation error"):
            service.invoke_model(model_id=model_id, payload=payload)
