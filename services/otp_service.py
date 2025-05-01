from services import mqtt_client
from services.config import settings
import time

university_id = settings.UNIVERSITY_ID
locker_id = settings.LOCKER_ID

# Simple data cache for storing OTP verification status
# key: otp, value: {verified, user_id, ...}
otp_cache = {}

# publish mqtt message, which topic is otp_verification
def send_otp_verification(otp: str, action: str):
    topic = f"event/{university_id}/{locker_id}/otp_verification"
    payload = {
        "otp": otp,
        "action": action,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    otp_cache[otp] = {"verified": None, "response": None}

    mqtt_client.publish(topic, payload)

# callback function for subscription
def handle_otp_result(payload):
    otp = payload.get("otp")
    if not otp:
        print("[OTP] Invalid payload: missing otp")
        return

    if otp in otp_cache:
        otp_cache[otp]["verified"] = payload.get("valid", False)
        otp_cache[otp]["response"] = payload
        print(f"[OTP] Cached result for OTP {otp}: {payload}")
    else:
        print(f"[OTP] Received result for unknown OTP: {otp}")

# deal with frontend's polling check
def get_otp_result(otp: str):
    entry = otp_cache.get(otp)
    if entry and entry["verified"] is not None:
        return entry["response"]
    return None

# create subscription for otp result
def subscribe_to_otp_result():
    topic = f"event/{university_id}/{locker_id}/otp_result"
    mqtt_client.subscribe(topic, handle_otp_result)
    print(f"[OTP] Subscribed to {topic}")
