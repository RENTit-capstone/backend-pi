from services import mqtt_client
from services.gpio_controller import gpio
from services.cache import cache_otp_result, set_slot_item, get_slot_item, set_current_open_slot
from services.config import settings
import time

university_id = settings.UNIVERSITY_ID
locker_id = settings.LOCKER_ID

def handle_otp_result(payload: dict) -> None:
    otp = payload.get("otp")
    if not otp:
        print("[LOGIC] Invalid OTP result payload")
        return

    cache_otp_result(otp, payload)
    print(f"[LOGIC] OTP result cached: {otp} → {payload}")

def start_subscribers() -> None:
    topic = f"event/{university_id}/{locker_id}/otp_result"
    mqtt_client.start()
    mqtt_client.subscribe(topic, handle_otp_result)
    print(f"[LOGIC] Subscribed to: {topic}")

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
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to perform action: {e}")
        return False