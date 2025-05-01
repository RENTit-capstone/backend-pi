otp_cache = {}

def cache_otp_result(otp: str, response: dict):
    otp_cache[otp] = {
        "verified": response.get("valid"),
        "response": response
    }

def get_otp_result(otp):
    entry = otp_cache.get(otp)
    if entry and entry["verified"] is not None:
        return entry["response"]
    return None
