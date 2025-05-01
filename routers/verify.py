from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from services import otp_service

router = APIRouter()

class OTPRequest(BaseModel):
    otp: str
    action: str

@router.post("/verify")
def verify_otp(request: OTPRequest):
    if not request.otp or not request.action:
        raise HTTPException(status_code=400, detail="Missing otp or action")

    otp_service.send_otp_verification(request.otp, request.action)
    return {"message": "OTP verification request sent"}

@router.get("/verify/result")
def get_result(otp: str = Query(..., description="OTP to check result for")): # need query parameter. ex) GET /api/verify/result?otp=1234
    result = otp_service.get_otp_result(otp)
    if result is None:
        return {"verified": None}
    return result