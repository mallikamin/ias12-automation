from app.logging_config import logger
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class APIError(Exception):
    """Base API error with standard format."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "BAD_REQUEST",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)


class NotFoundError(APIError):
    """Resource not found."""

    def __init__(self, resource: str, id: any = None):
        msg = (
            f"{resource} not found"
            if id is None
            else f"{resource} with id {id} not found"
        )
        super().__init__(msg, status_code=404, error_code="NOT_FOUND")


class ValidationError(APIError):
    """Invalid input data."""

    def __init__(self, message: str):
        super().__init__(message, status_code=422, error_code="VALIDATION_ERROR")


class PeriodLockedError(APIError):
    """Attempted to modify a locked period."""

    def __init__(self, period_name: str):
        super().__init__(
            f"Period '{period_name}' is locked and cannot be modified",
            status_code=403,
            error_code="PERIOD_LOCKED",
        )


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle APIError exceptions."""
    logger.warning(f"API Error: {exc.error_code} - {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "error_code": exc.error_code,
            "message": exc.message,
        },
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "error_code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
        },
    )
