import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_file_sync(path):
    with open(path, "rb") as f:
        resp = openai.Audio.transcriptions.create(
            file=f, model="whisper-1"
        )
    return resp["text"]