from fastapi import FastAPI
from app.api import health, tts, avatar, compose

app = FastAPI(title="AI Video Generator")

app.include_router(health.router)
app.include_router(tts.router, prefix="/tts", tags=["TTS"])
app.include_router(avatar.router, prefix="/avatar", tags=["Avatar"])
app.include_router(compose.router, prefix="/compose", tags=["Compose"])