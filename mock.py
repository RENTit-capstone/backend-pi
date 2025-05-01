from services import mqtt_client
import time

def handle_verification_request(payload):
    otp = payload.get("otp")
    if not otp:
        print("[MOCK] Invalid verification payload (missing OTP)")
        return

    print(f"[MOCK] Received OTP verification request for: {otp}")

    # 응답 메시지 구성
    response = {
        "otp": otp,
        "valid": True,
        "user_id": "mock_user_001",
        "user_name": "테스트사용자",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    mqtt_client.publish("event/ajou/locker1/otp_result", response)
    print(f"[MOCK] Sent mock OTP result for {otp}")

def main():
    print("[MOCK] Starting MQTT client and subscribing to otp_verification...")
    mqtt_client.subscribe("event/ajou/locker1/otp_verification", handle_verification_request)
    mqtt_client.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()