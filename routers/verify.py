from fastapi import APIRouter
from pydantic import BaseModel

from services import otp_service
from services.cache import get_otp_result, get_error

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
        error = get_error()
        if error:
            return {
                "verified": False,
                "error": error
            }
        return {"verified": None }
    

    return {
        "verified": True,
        **result
    }
