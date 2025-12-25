from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import edge_tts
import uuid
import os

from app.core.paths import OUTPUT_DIR

router = APIRouter()


class TTSRequest(BaseModel):
    text: str
    voice: str = "en-IN-PrabhatNeural"


@router.post("")
async def generate_tts(req: TTSRequest):
    """
    Generate speech audio using Microsoft Edge Neural TTS
    """

    try:
        if not req.text or len(req.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(OUTPUT_DIR, audio_filename)

        communicate = edge_tts.Communicate(
            text=req.text,
            voice=req.voice
        )

        await communicate.save(audio_path)

        return {
            "audio_path": f"output/{audio_filename}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )