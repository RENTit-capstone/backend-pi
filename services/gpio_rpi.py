from gpiozero import Servo, DigitalInputDevice
import time

from services.cache import get_current_open_slot

class GPIORpiController:
    PIN_MAP = {
        "A1": {"servo": 17, "reed": 27}
    }

    def __init__(self):
        self.servos = {}
        self.reeds = {}

        for slot_id, pins in self.PIN_MAP.items():
            self.servos[slot_id] = Servo(pins["servo"])
            self.reeds[slot_id] = DigitalInputDevice(pins["reed"], pull_up=False)

    def set_angle(self, slot_id: str, angle: int):
        angle = max(0, min(angle, 180))
        position = (angle - 90) / 90
        self.servos[slot_id].value = position
        time.sleep(0.5)
        self.servos[slot_id].detach()

    def open_slot(self, slot_id: str):
        self.set_angle(slot_id, 90)

    def close_slot(self, slot_id: str):
        self.set_angle(slot_id, 0)

    def read_reed(self, slot_id: str) -> bool:
        return self.reeds[slot_id].value
    
    def is_slot_closed(self) -> bool:
        slot_id = get_current_open_slot()
        if slot_id is None:
            print("[GPIO] 현재 열린 사물함 정보가 없습니다.")
            return False
        return self.read_reed(slot_id)