from fastapi import FastAPI

app = FastAPI(
    title="IAS 12 Automation API",
    description="Deferred tax computation, journals, and disclosures",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
