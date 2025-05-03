from fastapi import APIRouter
from pydantic import BaseModel

from services import otp_service
from services.cache import get_otp_result, get_available_slots

router = APIRouter()

class OTPRequest(BaseModel):
    otp: str
    action: str

@router.post("/verify")
def verify_otp(request: OTPRequest) -> dict:
    otp_service.send_otp_verification(request.otp, request.action)
    return {"message": "OTP verification request sent"}

@router.get("/verify/result")
def get_verification_result() -> dict:
    result = get_otp_result()
    if result is None:
        return {"verified": None}
    
    available_slots = get_available_slots()

    return {
        **result,
        "available_slots": available_slots
    }
