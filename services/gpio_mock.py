import random

class GPIOMockController:
    def __init__(self):
        print("[MOCK GPIO] Initialized mock controller")
        self.current_open_slot = None

    def set_angle(self, slot_id: str, angle: int):
        print(f"[MOCK GPIO] Slot {slot_id}: set_angle({angle}°)")

    def open_slot(self, slot_id: str):
        self.set_angle(slot_id, 90)
        print(f"[MOCK GPIO] Slot {slot_id}: OPEN")
        self.current_open_slot = slot_id

    def close_slot(self, slot_id: str):
        self.set_angle(slot_id, 0)
        print(f"[MOCK GPIO] Slot {slot_id}: CLOSE")
        self.current_open_slot = None

    def read_reed(self, slot_id: str) -> bool:
        result = random.random() < 0.8
        print(f"[MOCK GPIO] Slot {slot_id}: read_reed() -> {result}")
        return result

    def is_slot_closed(self) -> bool:
        slot_id = self.current_open_slot
        if slot_id is None:
            print("[GPIO] 현재 열린 사물함 정보가 없습니다.")
            return False
        return self.read_reed(slot_id)
