import time
from services import mqtt_client
from services.config import settings

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

    mqtt_client.publish(topic, payload)
    print(f"[OTP_SERVICE] Sent OTP verification: {payload}")
