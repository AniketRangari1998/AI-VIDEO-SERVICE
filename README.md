**🎬 AI Video Generation Service**

This repository provides a local AI backend for generating talking avatar videos and product promotion videos using open-source AI models.

It demonstrates how platforms like Arcads, Synthesia, HeyGen work internally — combining Text-to-Speech, Talking Head Generation, and Video Composition.

**✨ What This Project Does**

✔ Converts text into natural human-like speech
✔ Generates talking avatar videos from a single image
✔ Creates product promotion videos using avatar + product image
✔ Exposes everything via REST APIs
✔ Runs locally on CPU (slow but functional)
✔ Designed to be moved to GPU/cloud later

**🧠 AI Services Used (Important)**
**🎤 Text-to-Speech (TTS)**

Service: Microsoft Edge Neural TTS

Library: edge-tts

Voice Used: en-IN-PrabhatNeural

Provider: Microsoft (Edge / Azure Speech)

Cost: ✅ Free (via Edge TTS)

PrabhatNeural is a high-quality Indian English male voice provided by Microsoft.

📌 We do not host any TTS model ourselves — we call Edge TTS locally.

**🧑 Talking Avatar Video**

Model: SadTalker

Type: Audio-driven talking face generation

Input: Image + Audio

Output: MP4 talking avatar video

🔗 SadTalker GitHub
👉 https://github.com/vinthony/SadTalker

🙏 Huge thanks to the SadTalker authors for their incredible open-source work.
This project would not be possible without them.

**🎞 Video & Audio Processing**

Tool: FFmpeg

Used for:

Audio conversion (MP3 → WAV)

Video processing

Required on all OS

🔗 https://ffmpeg.org

**🏗 Project Structure**
<img width="565" height="484" alt="image" src="https://github.com/user-attachments/assets/2f24af6f-bf1d-4aa9-920b-57af0f8179cb" />


**⚙️ System Requirements**
Minimum (Development)

RAM: 8 GB

Disk: 20 GB free

Python: 3.10.x

CPU: Any modern CPU

⚠️ CPU mode is slow (1–5 min per video).
For production quality → GPU is required.

**🐍 Python Environment Setup (All OS)**
1️⃣ Install Python

Download from:
👉 https://www.python.org/downloads/

Verify:

python --version

2️⃣ Create Virtual Environment
python -m venv venv


**Activate:**

Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate

📦 Install Dependencies (requirements.txt)
Step 1: Install PyTorch (CPU only)

⚠️ Required before installing other packages

pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 \
 --index-url https://download.pytorch.org/whl/cpu

Step 2: Install all remaining dependencies
pip install -r requirements.txt

Step 3: Verify installation
python -c "import torch; print(torch.__version__)"

🎞 FFmpeg Installation (OS-Specific)
🪟 Windows
winget install "FFmpeg (Essentials Build)"


Restart terminal and verify:

ffmpeg -version
ffprobe -version

🐧 Linux (Ubuntu/Debian)
sudo apt update
sudo apt install ffmpeg -y

🍎 macOS
brew install ffmpeg

**🤖 SadTalker Manual Setup (Required)**

SadTalker must be installed manually.

**1️⃣ Clone SadTalker**
cd models
git clone https://github.com/vinthony/SadTalker.git

**2️⃣ Download Pretrained Models**

Download from:
👉 https://github.com/OpenTalker/SadTalker/blob/cd4c0465ae0b54a6f85af57f5c65fec9fe23e7f8/scripts/download_models.sh

Required files:

Direct download links, download and paste them in the folder -> models/SadTalker/checkpoints
SadTalker_V0.0.2_256.safetensors - https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors
SadTalker_V0.0.2_512.safetensors - https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors
mapping_00109-model.pth.tar - https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar
mapping_00229-model.pth.tar - https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar

Dowload weights, and paste them in the folder -> models/gfpan/weights
https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth
https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth


**3️⃣ Verify SadTalker**
python models/SadTalker/inference.py --help


If help appears → setup is correct ✅

**▶️ Start the Application**
uvicorn app.main:app --reload --port 9000


**Open:**

Use Postman or any other tool.

🔌 API Endpoints (Detailed)
**0️⃣ Health Check**

GET http://localhost:9000/health

Checks if backend is running.

Response:

{ "status": "UP" }

**🎤 1️⃣ Generate Audio (Text → Speech)**

POST http://localhost:9000/tts

What it does

Calls Microsoft Edge Neural TTS

Generates MP3 audio

Body:

{
  "text": "This protein shaker is perfect for gym lovers",
  "voice": "en-IN-PrabhatNeural"
}


Response:

{
  "audio_path": "output/audio.mp3"
}

**🧑 2️⃣ Generate Talking Avatar Video**

POST http://localhost:9000/avatar

What it does

Converts audio to WAV

Runs SadTalker

Generates talking head video

Body:

{
  "avatar_image": "uploads/avatar.jpg",
  "audio_path": "output/audio.mp3"
}


Response:

{
  "avatar_video": "output/avatar_video.mp4"
}


⏳ CPU time: 1–5 minutes

**🛍 3️⃣ Generate Product Promotion Video**

POST http://localhost:9000/compose

What it does

Overlays product image

Creates final promotional video

Body:

{
  "avatar_video": "output/avatar_video.mp4",
  "product_image": "uploads/product.png"
}


Response:

{
  "final_video": "output/final_promo.mp4"
}

**🔄 Typical Workflow**
POST /tts
   ↓
POST /avatar
   ↓
POST /compose

⚠️ Performance Notes

CPU mode is slow

First run loads models (longer)

For production:

Use GPU

Disable CPU-only mode

Deploy SadTalker separately



**🙌 Credits**

SadTalker – https://github.com/vinthony/SadTalker

Microsoft Edge TTS

FFmpeg

This project builds on amazing open-source contributions ❤️

**📄 License & Disclaimer**

This project is for educational & development purposes

Check licenses of:

SadTalker

FFmpeg

Microsoft TTS

**🏁 Final Note**

This repository shows how real AI video platforms are engineered —
from orchestration to ML integration to scaling.

If you can run this locally, you can run it in production.
