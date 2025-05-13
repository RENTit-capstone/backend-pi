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

state = CurrentState()

def set_otp_key(otp: str) -> None:
    state.otp = otp
    print("[Cache] Otp key cached successfully.")

def cache_otp_result(response: dict) -> None:
    state.response = response
    state.verified = True
    print(f"[Cache] OTP result cached for {state.otp}")

def get_otp_key() -> dict | None:
    if state.verified and state.response is not None:
        return state.response
    return None

def wipe_state() -> None:
    state.otp = None
    state.verified = False
    state.response = None
    state.rental_id = None
    state.action = None
    state.member_id = None
    state.locker_id = None
    print("[Cache] State wiped.")

def set_rental_id(rental_id: str) -> None:
    state.rental_id = rental_id

def get_rental_id() -> str | None:
    return state.rental_id

def set_action(action: str) -> None:
    state.action = action

def get_action() -> str | None:
    return state.action

def set_member_id(member_id: str) -> None:
    state.member_id = member_id

def get_member_id() -> str | None:
    return state.member_id

def set_locker_id(locker_id: str) -> None:
    state.locker_id = locker_id

def get_locker_id() -> str | None:
    return state.locker_id