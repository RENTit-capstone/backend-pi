from services import mqtt_client
from services.gpio_controller import gpio
from services.cache import cache_otp_result, get_otp_key, set_member_id, set_action, wipe_state, set_error
from services.config import settings
import time

university_id = settings.UNIVERSITY_ID
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
                "slot": r.get("lockerId")
            })

        cache_otp_result(parsed_result)
        print(f"[LOGIC] OTP result cached for user {member_id}")

    except Exception as e:
        print(f"[LOGIC] Failed to parse OTP result payload: {e}")
        wipe_state()

# TODO: implement below
def handle_empty_locker():
    pass

# TODO: implement below
def handle_event_result():
    pass

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

# TODO: Fix function below
def perform_action(item: dict, slot_id: str, action: str) -> bool:
    try:
        print(f"[LOGIC] Performing {action} on slot {slot_id} with item {item}")

        gpio.open_slot(slot_id)
        print(f"[LOGIC] Opened slot {slot_id}")
        
        set_current_open_slot(slot_id)

        time.sleep(2)

        if action in ["store", "return"]:
            set_slot_item(slot_id, item)
            print(f"[LOGIC] Stored item {item['item_id']} in slot {slot_id}")
        elif action in ["borrow", "retrieve"]:
            set_slot_item(slot_id, None)
            print(f"[LOGIC] Removed item from slot {slot_id}:")
        
        gpio.close_slot(slot_id)
        print(f"[LOGIC] Closed slot {slot_id}")

        # TODO: Shoud contain rentalId, memberId
        topic = "locker/request/event"
        payload = {
            "deviceId": locker_id,
            "lockerId": slot_id,
            "rentalId": None,
            "memberId": None,
            "action": action
        }
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to perform action: {e}")
        return False