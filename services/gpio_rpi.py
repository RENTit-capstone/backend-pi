import RPi.GPIO as GPIO
import time

class GPIORpiController:
    PIN_MAP = {
        "A1": {"servo": 17, "reed": 27}
    }

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pwm = {}
        for slot_id, pins in self.PIN_MAP.items():
            GPIO.setup(pins["servo"], GPIO.OUT)
            GPIO.setup(pins["reed"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            pwm = GPIO.PWM(pins["servo"], 50)
            pwm.start(0)
            self.pwm[slot_id] = pwm

    def set_angle(self, slot_id: str, angle: int):
        duty = 2.5 + (angle / 180.0) * 10
        self.pwm[slot_id].ChangeDutyCycle(duty)
        time.sleep(0.5)
        self.pwm[slot_id].ChangeDutyCycle(0)

    def open_slot(self, slot_id: str):
        self.set_angle(slot_id, 90)

    def close_slot(self, slot_id: str):
        self.set_angle(slot_id, 0)

    def read_reed(self, slot_id: str) -> bool:
        return GPIO.input(self.PIN_MAP[slot_id]["reed"]) == GPIO.HIGH
    