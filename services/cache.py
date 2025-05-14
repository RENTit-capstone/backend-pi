from services.config import settings

class CurrentState:
    def __init__(self):
        self.otp: str | None = None
        self.verified: bool | None = None
        self.response: dict | None = None

        self.rental_id: str | None = None
        self.action: str | None = None
        self.member_id: str | None = None
        self.locker_id: str | None = None
        self.error: str | None = None
        self.available_slots: list[str] = []

global_state = CurrentState()

def set_otp_key(otp: str) -> None:
    global_state.otp = otp
    print("[Cache] Otp key cached successfully.")

def get_otp_key() -> str | None:
    otp = global_state.otp
    if otp is not None:
        print(f"[Cache] Otp key({otp}) loaded successfully.")
        return otp
    print("[Cache] No otp key is set.")
    return None

def cache_otp_result(response: dict) -> None:
    global_state.response = response
    global_state.verified = True
    print(f"[Cache] OTP result cached for {global_state.otp}")

def get_otp_result() -> dict | None:
    if global_state.verified and global_state.response is not None:
        return global_state.response
    print(f"[Cache] Error Occured: verified: {global_state.verified}, response: {global_state.response}")
    return None

def wipe_state() -> None:
    global_state.otp = None
    global_state.verified = False
    global_state.response = None
    global_state.rental_id = None
    global_state.action = None
    global_state.member_id = None
    global_state.locker_id = None
    print("[Cache] State wiped.")

def set_rental_id(rental_id: str) -> None:
    global_state.rental_id = rental_id

def get_rental_id() -> str | None:
    return global_state.rental_id

def set_action(action: str) -> None:
    global_state.action = action

def get_action() -> str | None:
    return global_state.action

def set_member_id(member_id: str) -> None:
    global_state.member_id = member_id

def get_member_id() -> str | None:
    return global_state.member_id

def set_locker_id(locker_id: str) -> None:
    global_state.locker_id = locker_id

def get_locker_id() -> str | None:
    return global_state.locker_id

def set_error(msg: str) -> None:
    global_state.error = msg

def get_error() -> str | None:
    return global_state.error

def set_available_slots(slots: list[str]) -> None:
    global_state.available_slots = slots

def get_available_slots() -> list[str]:
    return global_state.available_slots