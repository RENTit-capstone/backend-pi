import time
from services import mqtt_client
from services.config import settings
from services.cache import set_otp_key

#university_id = settings.UNIVERSITY_ID
locker_id = settings.LOCKER_ID


def send_otp_verification(otp: str, action: str) -> None:
    topic = "Locker/request/eligible"
    payload = {
        "deviceId": locker_id,
        "otpCode": otp,
        "action": action,
        "rentalId": None
    }

    set_otp_key(otp)

    mqtt_client.publish(topic, payload)
    print(f"[OTP_SERVICE] Sent OTP verification: {payload}")
