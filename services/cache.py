otp_cache: dict[str, dict] = {}

def cache_otp_result(otp: str, response: dict) -> None:
    otp_cache[otp] = {
        "verified": response.get("valid"),
        "response": response
    }

def get_otp_result(otp: str) -> dict | None:
    entry = otp_cache.get(otp)
    if entry and entry["verified"] is not None:
        return entry["response"]
    return None
