class GPIOMockController:
    def __init__(self):
        print("[MOCK GPIO] Initialized mock controller")

    def set_angle(self, slot_id: str, angle: int):
        print(f"[MOCK GPIO] Slot {slot_id}: set_angle({angle}*)")

    def open_slot(self, slot_id: str):
        self.set_angle(slot_id, 90)
        print(f"[MOCK GPIO] Slot {slot_id}: OPEN")
    
    def close_slot(self, slot_id: str):
        self.set_angle(slot_id, 0)
        print(f"[MOCK GPIO] Slot {slot_id}: CLOSE")
    
    def read_reed(self, slot_id: str) -> bool:
        print(f"[MOCK GPIO] Slot {slot_id}: read_reed() -> False")
        return False
