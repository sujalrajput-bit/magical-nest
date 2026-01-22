"""FastAPI application entry point for MN AI Voice Agent."""

from fastapi import FastAPI

from mn_ai_voice.app.api.calls import router as calls_router

app = FastAPI(
    title="MN AI Voice Agent",
    version="0.1.0",
    description="AI-powered voice call agent for lead qualification.",
)

app.include_router(calls_router, prefix="/calls", tags=["calls"])


@app.get("/health", tags=["system"])
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
