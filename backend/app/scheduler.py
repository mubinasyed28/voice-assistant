from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bson import ObjectId
from datetime import datetime, timezone
from app.tts_murf import generate_tts
from app.twilio_call import initiate_reminder_call
from app.db import reminders_collection
import asyncio

scheduler = AsyncIOScheduler()

async def check_reminders():
    now = datetime.now(timezone.utc).isoformat()

    cursor = reminders_collection.find({
        "status": "pending",
        "time": {"$lte": now}
    })

    async for doc in cursor:
        reminder_id = str(doc["_id"])
        text = f"Reminder: {doc['task']}"

        # Generate TTS
        filename, _path = generate_tts(text, f"rem_{reminder_id}.mp3")

        # Initiate call
        call_sid = initiate_reminder_call(doc['phone'], filename)

        # Update DB
        await reminders_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"status": "called", "call_sid": call_sid}}
        )

def start_scheduler():
    # ❌ Do NOT wrap in lambda
    # ❌ Do NOT call asyncio.create_task()
    scheduler.add_job(check_reminders, "interval", minutes=1)

    # Start the scheduler with the running event loop
    scheduler.start()