from app.config import settings
from app.errors import APIError, api_error_handler, generic_error_handler
from app.logging_config import logger
from fastapi import FastAPI

app = FastAPI(
    title="IAS 12 Automation API",
    description="Deferred tax computation, journals, and disclosures",
    version="0.1.0",
    debug=settings.DEBUG,
)

# Register error handlers
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(Exception, generic_error_handler)


@app.on_event("startup")
def startup_event():
    """Log application startup."""
    logger.info(f"Starting IAS 12 API in {settings.ENV} mode")
    logger.info(f"Debug: {settings.DEBUG}")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    logger.debug("Health check called")
    return {"status": "ok", "env": settings.ENV}
