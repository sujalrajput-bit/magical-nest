
from fastapi import FastAPI
from mn_ai_voice.app.api.calls import router as calls_router

app = FastAPI(title="MN AI Voice Agent")

app.include_router(calls_router, prefix="/calls")
