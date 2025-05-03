from services.config import Settings
# ========== OTP ==========
class CurrentOtpState:
    def __init__(self):
        self.otp: str | None = None
        self.verified: bool | None = None
        self.response: dict | None = None

current_otp_state = CurrentOtpState()

def wipe_otp_result() -> None:
    current_otp_state.otp = None
    current_otp_state.verified = False
    current_otp_state.response = None

def cache_otp_result(otp: str, response: dict) -> None:
    current_otp_state.otp = otp
    current_otp_state.response = response
    current_otp_state.verified = response.get("valid")

def get_otp_result() -> dict | None:
    if current_otp_state.verified and current_otp_state.response is not None:
        return current_otp_state.response
    return None

# ========== Slots ==========
slot_items : dict[str, dict | None] = {
    slot_id: None for slot_id in Settings.slots
}

def get_slot_item(slot_id: str) -> dict | None:
    return slot_items.get(slot_id)

def set_slot_item(slot_id: str, item: dict | None) -> None:
    if slot_id in slot_items:
        slot_items[slot_id] = item

def get_all_slot_states() -> dict[str, dict | None]:
    return slot_items.copy()

def get_available_slots() -> list[str]:
    return [slot for slot, item in slot_items.items() if item is None]
