import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

# Get the root logger or a named logger
logger = logging.getLogger("VALIDATION_HANDLER")


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Validates request payload and returns a human-readable error message.

    Args:
        request (Request): incoming data from the client.
        exc (RequestValidationError): pydantic validation error.

    Returns:
        JSONResponse: Error message with a 400 status code.
    """
    # Log the validation error details
    logger.error(
        f"Validation error on {request.url.path}: {exc.errors()} - Input: {exc.body}")

    return JSONResponse(
        status_code=400,
        content={
            "message": f"{exc.errors()[0].get('msg')}. Please check your request and try again."
        },
    )
