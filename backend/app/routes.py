from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import Response
import aiofiles, os
from app.asr import transcribe_file_sync
from app.ai_brain import extract_reminder_sync, general_reply
from app.db import reminders_collection
from datetime import datetime
from app.tts_murf import generate_tts
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

UPLOAD_DIR = "uploads"
AUDIO_DIR = "reminders_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(path, "wb") as f:
        await f.write(await file.read())
    text = transcribe_file_sync(path)
    return {"transcription": text}

@router.post("/set_reminder/")
async def set_reminder(message: str = Form(...)):
    data = extract_reminder_sync(message)

    if not data["time"]:
        return {"error": "Specify time clearly."}
    if not data["phone"]:
        return {"error": "Please include phone number in message."}

    reminder = {
        "task": data["task"],
        "time": data["time"],
        "phone": data["phone"],
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }
    res = await reminders_collection.insert_one(reminder)
    return {"id": str(res.inserted_id), "msg": "Reminder set"}

@router.get("/twiml/{audio_file}")
async def play_audio_twiml(audio_file: str):
    audio_url = f"{os.getenv('BASE_URL')}/audio/{audio_file}"

    twiml = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Play>{audio_url}</Play>
    </Response>
    """

    return Response(content=twiml, media_type="application/xml")