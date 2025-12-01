from twilio.rest import Client
import os

sid = os.getenv("TWILIO_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_from = os.getenv("TWILIO_FROM")
BASE_URL = os.getenv("BASE_URL")

client = Client(sid, token)

def initiate_reminder_call(phone, audio_filename):
    # TwiML URL points to backend endpoint
    twiml_url = f"{BASE_URL}/twiml/{audio_filename}"

    call = client.calls.create(
        to=phone,
        from_=twilio_from,
        url=twiml_url
    )
    return call.sid