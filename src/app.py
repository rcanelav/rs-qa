import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from src.bedrock_service import BedrockService
from src.logs import configure_logging
from src.models import QuestionAnswerRequest
from src.validation_handlers import validation_exception_handler

load_dotenv()

# App initialization
configure_logging()
logger = logging.getLogger("APP")

app = FastAPI()
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.post("/predict")
async def question_answering(request: QuestionAnswerRequest) -> dict:
    """Generates a response to a given question using the AWS Bedrock model.

    Args:
        request (QuestionAnswerRequest): The request payload containing the question.

    Raises:
        HTTPException: Should be raised when an error occurs while inferencing.

    Returns:
        dict: The response from the model.
    """
    try:
        payload = {
            "modelId": os.environ.get("AWS_BEDROCK_MODEL_ID"),
            "contentType": "application/json",
            "accept": "application/json",
            "body": {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 512,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": request.question
                            }
                        ]
                    }
                ]
            }
        }

        llm_service = BedrockService()
        response = llm_service.invoke_model(
            model_id=payload["modelId"],
            payload=payload["body"],
        )

        response_body = response.get("content")[0].get("text")
        return {"response": response_body}

    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=500, detail=error_message)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("src:app", host="0.0.0.0", port=8000, reload=True)
