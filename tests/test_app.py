import os
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.app import app


class TestQuestionAnsweringApplication:
    """
    Test suite for the QuestionAnsweringApplication.
    """

    @pytest.fixture
    def mock_bedrock_service(self):
        """Fixture to mock BedrockService."""
        with patch("src.app.BedrockService", autospec=True) as mock_service:
            yield mock_service

    @pytest.fixture
    def client(self):
        """Fixture to provide a FastAPI test client."""
        return TestClient(app)

    def test_health_check(self, client):
        """Test the /health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_question_answering_success(self, client, mock_bedrock_service):
        """Test the /predict endpoint for a successful case."""
        # Arrange
        question = "What is the capital of France?"
        answer = "This is the response from the model."
        mock_instance = mock_bedrock_service.return_value
        mock_instance.invoke_model.return_value = {
            "content": [{"text": answer}]
        }

        payload = {"question": question}

        # Act
        response = client.post("/predict", json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "response": answer}
        mock_instance.invoke_model.assert_called_once_with(
            model_id=os.environ.get("AWS_BEDROCK_MODEL_ID"),
            payload={
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 512,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": question}],
                    }
                ],
            },
        )

    def test_question_answering_validation_error(self, client):
        """Test the /predict endpoint for validation errors."""
        # Act
        response = client.post("/predict", json={})
        # Assert
        assert response.status_code == 400
        # Pydantic validation error
        assert response.json().get(
            "message") == "Field required. Please check your request and try again."

    def test_question_answering_validation_error_type(self, client):
        """Test the /predict endpoint for validation errors. Input type case"""
        # Act
        response = client.post("/predict", json={
            "question": 123
        })

        print(f"🚀 {response.json()}")
        # Assert
        assert response.status_code == 400
        # Pydantic validation error
        assert response.json().get(
            "message") == "Input should be a valid string. Please check your request and try again."

    def test_question_answering_internal_error(self, client, mock_bedrock_service):
        """Test the /predict endpoint for internal server errors."""
        # Arrange
        mock_instance = mock_bedrock_service.return_value
        mock_instance.invoke_model.side_effect = Exception(
            "Mocked service failure")

        payload = {"question": "What is the capital of France?"}

        # Act
        response = client.post("/predict", json=payload)
        print(f"🚀 {response.json()}")
        # Assert
        assert response.status_code == 500
        assert "Error occurred: Mocked service failure" in response.json()[
            "detail"]
        mock_instance.invoke_model.assert_called_once()
