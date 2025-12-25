from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import os
import sys
import glob
import time

from app.core.paths import BASE_DIR, OUTPUT_DIR
from app.core.audio import convert_to_wav

router = APIRouter()

# ✅ BULLETPROOF: use the SAME python that runs FastAPI
PYTHON_EXECUTABLE = sys.executable


class AvatarRequest(BaseModel):
    avatar_image: str   # e.g. uploads/avatar01.png
    audio_path: str     # e.g. output/audio.mp3


def get_latest_video(output_dir: str) -> str:
    """
    Find the most recently created MP4 file in output directory
    """
    time.sleep(1)  # allow filesystem to flush
    videos = glob.glob(os.path.join(output_dir, "*.mp4"))

    if not videos:
        raise Exception("SadTalker did not generate any video")

    return max(videos, key=os.path.getctime)


@router.post("")
def generate_avatar(req: AvatarRequest):
    try:
        # -------------------------------------------------
        # Resolve absolute paths
        # -------------------------------------------------
        avatar_image_path = os.path.join(BASE_DIR, req.avatar_image)
        audio_input_path = os.path.join(BASE_DIR, req.audio_path)

        if not os.path.exists(avatar_image_path):
            raise HTTPException(
                status_code=400,
                detail=f"Avatar image not found: {avatar_image_path}"
            )

        if not os.path.exists(audio_input_path):
            raise HTTPException(
                status_code=400,
                detail=f"Audio file not found: {audio_input_path}"
            )

        # -------------------------------------------------
        # Convert audio to WAV (SadTalker requirement)
        # -------------------------------------------------
        wav_audio_path = convert_to_wav(audio_input_path)

        if not os.path.exists(wav_audio_path):
            raise HTTPException(
                status_code=500,
                detail="Failed to convert audio to WAV"
            )

        # -------------------------------------------------
        # Build SadTalker command
        # -------------------------------------------------
        cmd = [
            PYTHON_EXECUTABLE,
            "inference.py",
            "--source_image", avatar_image_path,
            "--driven_audio", wav_audio_path,
            "--result_dir", OUTPUT_DIR,
            "--still",
            "--preprocess", "crop",
            "--cpu"
        ]

        # -------------------------------------------------
        # Run SadTalker (CLI tool)
        # -------------------------------------------------
        result = subprocess.run(
            cmd,
            cwd=os.path.join(BASE_DIR, "models", "SadTalker"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("\n===== SadTalker STDOUT =====")
        print(result.stdout)

        print("\n===== SadTalker STDERR =====")
        print(result.stderr)

        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"SadTalker failed:\n{result.stderr}"
            )

        # -------------------------------------------------
        # Find actual generated video
        # -------------------------------------------------
        latest_video = get_latest_video(OUTPUT_DIR)

        return {
            "avatar_video": os.path.relpath(latest_video, BASE_DIR)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )