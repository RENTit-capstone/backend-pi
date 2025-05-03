from fastapi import APIRouter, Query
from pydantic import BaseModel

from services import otp_service
from services.cache import get_otp_result

router = APIRouter()


class OTPRequest(BaseModel):
    otp: str
    action: str


@router.post("/verify")
def verify_otp(request: OTPRequest) -> dict:
    otp_service.send_otp_verification(request.otp, request.action)
    return {"message": "OTP verification request sent"}


@router.get("/verify/result")
def get_result() -> dict:
    result = get_otp_result()
    return result if result is not None else {"verified": None}
