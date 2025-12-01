from fastapi import FastAPI
from app.routes import router
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.scheduler import start_scheduler
import os

app = FastAPI(title="Voice Productivity Assistant + Twilio Calls")
app.include_router(router)

# Serve reminder audio
if not os.path.exists("reminders_audio"):
    os.makedirs("reminders_audio")
app.mount("/audio", StaticFiles(directory="reminders_audio"), name="audio")

@app.on_event("startup")
async def startup_event():
    start_scheduler()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)