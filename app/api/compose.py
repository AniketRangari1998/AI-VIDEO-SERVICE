from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import uuid
from app.core.paths import OUTPUT_DIR

router = APIRouter()

class ComposeRequest(BaseModel):
    avatar_video: str
    product_image: str

@router.post("")
def compose_video(req: ComposeRequest):

    final_video = f"{OUTPUT_DIR}/{uuid.uuid4()}_promo.mp4"

    cmd = [
        "ffmpeg",
        "-i", req.avatar_video,
        "-i", req.product_image,
        "-filter_complex", "overlay=W-w-20:H-h-20",
        final_video
    ]

    subprocess.run(cmd, check=True)

    return {"final_video": final_video}