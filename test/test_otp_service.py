import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services import mqtt_client
from services import otp_service
import time

def main():
    test_otp = "12345"
    test_action = "store"

    print("[TEST] Subscribing to OTP result topic...")
    otp_service.subscribe_to_otp_result()
    mqtt_client.start()

    time.sleep(1)
    print(f"[TEST] Sending OTP verification: {test_otp}, action: {test_action}")
    otp_service.send_otp_verification(test_otp, test_action)

    print("[TEST] Waiting for OTP result...")
    for _ in range(10):
        result = otp_service.get_otp_result(test_otp)
        if result:
            print(f"[TEST] OTP result received: {result}")
            break
        time.sleep(1)
    else:
        print("[TEST] Timeout: No OTP result received")

if __name__ == "__main__":
    main()