from gpiozero import Servo, DigitalInputDevice
import time

class GPIORpiController:
    PIN_MAP = {
        "1": {"servo": 17, "reed": 27}
    }

    def __init__(self):
        self.servos = {}
        self.reeds = {}
        self.current_open_slot = None

        for slot_id, pins in self.PIN_MAP.items():
            self.servos[slot_id] = Servo(pins["servo"])
            self.reeds[slot_id] = DigitalInputDevice(pins["reed"], pull_up=False)
            self.close_slot(slot_id)

    def set_angle(self, slot_id: str, angle: int):
        angle = max(0, min(angle, 180))
        position = (angle / 45.0) - 1.0
        #self.servos[slot_id].value = position
        self.servos["1"].value = position
        time.sleep(0.5)
        #self.servos[slot_id].detach()
        self.servos["1"].detach()

    def open_slot(self, slot_id: str):
        self.set_angle(slot_id, 90)
        print(f"[GPIO] Slot {slot_id}: OPEN")
        self.current_open_slot = slot_id

    def close_slot(self, slot_id: str):
        self.set_angle(slot_id, 0)
        print(f"[GPIO] Slot {slot_id}: CLOSE")
        self.current_open_slot = None

    def read_reed(self, slot_id: str) -> bool:
        #value = self.reeds[slot_id].value
        value = self.reeds["1"].value
        print(f"[GPIO] Slot {slot_id}: read_reed() -> {value}")
        return value

    def is_slot_closed(self) -> bool:
        slot_id = self.current_open_slot
        if slot_id is None:
            print("[GPIO] 현재 열린 사물함 정보가 없습니다.")
            return False
        return self.read_reed(slot_id)
