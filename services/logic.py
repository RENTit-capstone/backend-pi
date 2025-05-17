from services import mqtt_client
from services.gpio_controller import gpio
from services.cache import (
    cache_otp_result, set_member_id, set_action, wipe_state, set_error, set_available_slots,
    get_locker_id, get_rental_id, get_member_id, get_action, get_otp_key, set_is_opened, get_fee
)
from services.config import settings
import time

locker_id = settings.LOCKER_ID

def handle_otp_result(payload: dict) -> None:
    if payload.get("success") is not True:
        set_error(payload.get("message", "OTP 인증 실패"))
        print(f"[LOGIC] OTP verification failed: {payload.get('message')}")
        wipe_state()
        return

    otp = get_otp_key()
    if otp is None:
        print(f"[LOGIC] OTP result received, but no OTP key is set.")
        wipe_state()
        return

    data = payload.get("data")
    if data is None:
        print("[LOGIC] OTP result missing data field.")
        wipe_state()
        return

    try:
        member_id = data["memberId"]
        action = data["action"]
        rentals = data["rentals"]

        set_member_id(member_id)
        set_action(action)

        parsed_result = {
            "user_name": member_id,
            "items": []
        }

        for r in rentals:
            parsed_result["items"].append({
                "item_id": r["itemId"],
                "name": r["itemName"],
                "slot": r.get("lockerId"),
                "fee": r.get("fee"),
                "balance": r.get("balance"),
                "payable": r.get("payable", True)
            })


        cache_otp_result(parsed_result)
        print(f"[LOGIC] OTP result cached for user: {member_id}")

    except Exception as e:
        print(f"[LOGIC] Failed to parse OTP result payload: {e}")
        wipe_state()

def get_empty_slot(rentalId: str, action: str) -> None:
    topic = "locker/request/available"
    payload = {
        "deviceId": locker_id,
        "otpCode": None,
        "action": action,
        "rentalId": rentalId
    }
    mqtt_client.publish(topic, payload)
    print(f"[LOGIC] Emtpy Slot require published")

def start_subscribers() -> None:
    verification_topic = f"locker/{locker_id}/eligible"
    empty_locker_topic = f"locker/{locker_id}/available"
    locker_event_topic = f"locker/{locker_id}/event"
    mqtt_client.start()
    mqtt_client.subscribe(verification_topic, handle_otp_result)
    mqtt_client.subscribe(empty_locker_topic, handle_empty_locker)
    mqtt_client.subscribe(locker_event_topic, handle_event_result)
    print(f"[LOGIC] Subscribed to:")
    print(f"\tverification: {verification_topic}")
    print(f"\tempty_locker: {empty_locker_topic}")
    print(f"\tlocker_event: {locker_event_topic}")

def perform_action() -> bool:
    try:
        slot_id = get_locker_id()
        action = get_action()

        if not all([slot_id]):
            print("[LOGIC] Missing required state for perform_aciton")
            return False
        
        print(f"[LOGIC] Performing {action} on locker {slot_id}")

        gpio.open_slot(slot_id)
        print(f"[LOGIC] Locker {slot_id} opened")
        set_is_opened(False)

        time.sleep(2)

        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to perform action: {e}")
        return False
    
def handle_empty_locker(payload: dict) -> None:
    if payload.get("success") is not True:
        print(f"[LOGIC] Failed to get empty lockers: {payload.get('message')}")
        set_error(payload.get("message", "빈 사물함 목록 요청 실패"))
        wipe_state()
        return
    
    data = payload.get("data")
    if data is None or "lockers" not in data:
        print("[LOGIC] Missing lockers in empty locker response.")
        set_error("사물함 목록이 없습니다")
        wipe_state()
        return
    
    available_lockers = [
        locker["lockerId"]
        for locker in data["lockers"]
        if locker.get("available") is True
    ]

    set_available_slots(available_lockers)
    print(f"[LOGIC] Available slots set: {available_lockers}")
    for locker in available_lockers:
        print(f"  - ID: {locker.get('lockerId')}, Fee: {locker.get('fee')}, Balance: {locker.get('balance')}, Payable: ✅")

def handle_event_result(payload: dict):
    if payload.get("success") is not True:
        msg = payload.get("message", "사물함 이벤트 처리 실패")
        print(f"[LOGIC] Event failed: {msg}")
        set_error(msg)
        wipe_state()
        return
    data = payload.get("data", {})
    locker_id = data.get("lockerId")
    rental_id = data.get("rentalId")

    print(f"[LOGIC] Event acknowledged by server (lockerId={locker_id}, rentalId={rental_id})")
