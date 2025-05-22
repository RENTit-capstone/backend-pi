from services import mqtt_client
import time
from services.config import settings

# ===============================
# 🧠 내부 상태 (전부 인메모리 저장)
# ===============================

balance = 5000

otp_map = {
    "00000": {
        "memberId": 1,
        "action": "DROP_OFF_BY_OWNER",
        "nickname":"가ㅏ가ㅏ가가",
        "rentals": [
            {
                "rentalId": 1,
                "itemId": 1,
                "itemName": "삼각대",
                "lockerId": None,
                "fee": 1000
            },
            {
                "rentalId": 2,
                "itemId": 2,
                "itemName": "조명",
                "lockerId": None,
                "fee": 10000
            }
        ]
    },
    "11111": {
        "memberId": 2,
        "action": "PICK_UP_BY_RENTER",
        "nickname":"나난난나나ㅏ나ㅏㅏ",
        "rentals": [
            {
                "rentalId": 3,
                "itemId": 3,
                "itemName": "노트북 거치대",
                "lockerId": "1",
                "fee": 1000
            }
        ]
    }
}

locker_status = {
    "1": True,
    "2": False,
    "3": True,
    "4": True
}

LOCKER_ID = settings.LOCKER_ID

# ===============================
# 📨 응답 발행 도우미
# ===============================

def publish_response(topic: str, data: dict, success: bool = True, message: str = ""):
    response = {
        "success": success,
        "data": data if success else None,
        "message": message
    }
    mqtt_client.publish(topic, response)
    print(f"[MOCK] Published to {topic}: {response}")

# ===============================
# ✅ OTP 인증 요청 핸들러
# ===============================

def handle_otp_verification(payload):
    print(f"[MOCK] handle_otp_verification called")
    otp = payload.get("otpCode")
    topic = f"locker/{LOCKER_ID}/eligible"

    if otp not in otp_map:
        publish_response(topic, {}, success=False, message="OTP가 유효하지 않습니다.")
        return

    user_info = otp_map[otp]
    rentals = []

    for r in user_info["rentals"]:
        payable = balance >= r["fee"]

        rental = {
            "rentalId": r["rentalId"],
            "itemId": r["itemId"],
            "itemName": r["itemName"],
            "lockerId": r.get("lockerId"),
            "fee": r["fee"],
            "balance": balance,
            "payable": payable
        }
        rentals.append(rental)

    data = {
        "deviceId": LOCKER_ID,
        "action": user_info["action"],
        "memberId": user_info["memberId"],
        "nickname": user_info["nickname"],
        "rentals": rentals
    }
    publish_response(topic, data)

# ===============================
# ✅ 빈 사물함 요청 핸들러
# ===============================

def handle_empty_locker_request(payload):
    print(f"[MOCK] handle_empty_locker_request called")
    rental_id = payload.get("rentalId")
    topic = f"locker/{LOCKER_ID}/available"

    if not rental_id:
        publish_response(topic, {}, success=False, message="rentalId가 없습니다.")
        return

    # 사용 가능한 locker 목록 반환
    available = [
        {
            "deviceId": LOCKER_ID,
            "lockerId": locker_id,
            "available": status
        }
        for locker_id, status in locker_status.items()
    ]

    data = {
        "deviceId": LOCKER_ID,
        "rentalId": rental_id,
        "lockers": available
    }
    publish_response(topic, data)

# ===============================
# ✅ 이벤트 처리 응답 핸들러
# ===============================

def handle_event(payload):
    print(f"[MOCK] handle_event called")
    locker_id = payload.get("lockerId")
    rental_id = payload.get("rentalId")
    topic = f"locker/{LOCKER_ID}/event"

    if not locker_id or not rental_id:
        publish_response(topic, {}, success=False, message="lockerId 또는 rentalId 누락됨.")
        return

    data = {
        "deviceId": LOCKER_ID,
        "lockerId": locker_id,
        "rentalId": rental_id
    }
    publish_response(topic, data)

# ===============================
# 🚀 시작
# ===============================

def main():
    print("[MOCK] Starting MQTT client and subscribing to topics...")

    mqtt_client.subscribe("locker/request/eligible", handle_otp_verification)
    mqtt_client.subscribe("locker/request/available", handle_empty_locker_request)
    mqtt_client.subscribe("locker/request/event", handle_event)

    mqtt_client.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
