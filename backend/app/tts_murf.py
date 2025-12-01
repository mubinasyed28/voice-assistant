import os, requests, uuid
from dotenv import load_dotenv

load_dotenv()
MURF_KEY = os.getenv("MURF_API_KEY")
OUT_DIR = "reminders_audio"
os.makedirs(OUT_DIR, exist_ok=True)

def generate_tts(text, filename=None):
    if not filename:
        filename = f"{uuid.uuid4().hex}.mp3"

    endpoint = "https://api.murf.ai/v1/tts"
    headers = {"Authorization": f"Bearer {MURF_KEY}", "Content-Type":"application/json"}

    payload = {
        "voice": "falcon-1",
        "input": text,
        "format": "mp3"
    }

    r = requests.post(endpoint, json=payload, headers=headers, stream=True)
    if r.status_code not in (200, 201):
        raise Exception(r.text)

    path = os.path.join(OUT_DIR, filename)
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

    return filename, path