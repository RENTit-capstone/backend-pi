# services/logic.py
from services import mqtt_client
from services.cache import cache_otp_result
from services.config import settings

university_id = settings.UNIVERSITY_ID
locker_id = settings.LOCKER_ID

def handle_otp_result(payload: dict):
    otp = payload.get("otp")
    if not otp:
        print("[LOGIC] Invalid OTP result payload")
        return
    cache_otp_result(otp, payload)
    print(f"[LOGIC] OTP result cached: {otp} → {payload}")

def start_subscribers():
    topic = f"event/{university_id}/{locker_id}/otp_result"
    mqtt_client.start()
    mqtt_client.subscribe(topic, handle_otp_result)
    print(f"[LOGIC] Subscribed to: {topic}")
