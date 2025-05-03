from services import mqtt_client
import time

def handle_verification_request(payload):
    otp = payload.get("otp")
    action = payload.get("action")

    if not otp or not action:
        print("[MOCK] Invalid verification payload (missing OTP or action)")
        return

    print(f"[MOCK] Received OTP verification request for: {otp} ({action})")

    # 공통 응답 필드
    response = {
        "otp": otp,
        "valid": True,
        "user_name": "테스트사용자",
        "action": action,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # 행동(action)에 따라 응답 형태를 다르게 설정
    if action == "store":
        response["items"] = [
            {"item_id": "item_001", "name": "삼각대"},
            {"item_id": "item_002", "name": "조명"}
        ]
        response["available_slots"] = [2, 5, 6]

    elif action == "borrow":
        response["items"] = [
            {"item_id": "item_101", "name": "멀티탭", "slot": 3},
            {"item_id": "item_102", "name": "노트북 거치대", "slot": None}
        ]

    elif action == "return":
        response["items"] = [
            {"item_id": "item_201", "name": "공구 세트"}
        ]
        response["available_slots"] = [1, 4]

    elif action == "retrieve":
        response["items"] = [
            {"item_id": "item_301", "name": "마이크", "slot": 2},
            {"item_id": "item_302", "name": "HDMI 케이블", "slot": None}
        ]

    else:
        print(f"[MOCK] Unknown action: {action}")
        return

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
