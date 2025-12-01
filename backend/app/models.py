from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Reminder(BaseModel):
    task: str
    time: datetime
    phone: str
    created_at: Optional[datetime] = None
    status: Optional[str] = "pending"
    audio_filename: Optional[str] = None