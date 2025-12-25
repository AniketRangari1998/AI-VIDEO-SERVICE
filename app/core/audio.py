from pydub import AudioSegment
import os

def convert_to_wav(input_audio_path: str) -> str:
    """
    Convert any audio to 16kHz mono WAV (SadTalker compatible)
    """
    if input_audio_path.lower().endswith(".wav"):
        return input_audio_path

    audio = AudioSegment.from_file(input_audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)

    wav_path = os.path.splitext(input_audio_path)[0] + ".wav"
    audio.export(wav_path, format="wav")

    return wav_path