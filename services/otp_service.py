from services import mqtt_client
import uuid
import time

# Simple data cache for storing OTP verification status
# key: otp, value: {verified, user_id, ...}
otp_cache = {}

# publish mqtt message, which topic is otp_verification
def send_otp_verification(otp: str, locker_id: str, university_id: str, action: str):
    pass

# callback function for subscription
def handle_otp_result(payload):
    pass

# deal with frontend's polling check
def get_otp_result(otp: str):
    pass

# create subscription for otp result
def subscribe_to_otp_result(university_id: str, locker_id: str):
    pass
