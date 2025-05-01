# services/otp_service.py
from services import mqtt_client
from services.config import settings
import time

university_id = settings.UNIVERSITY_ID
locker_id = settings.LOCKER_ID

def send_otp_verification(otp: str, action: str):
    topic = f"event/{university_id}/{locker_id}/otp_verification"
    payload = {
        "otp": otp,
        "action": action,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    mqtt_client.publish(topic, payload)
    print(f"[OTP_SERVICE] Published verification request: {payload}")
