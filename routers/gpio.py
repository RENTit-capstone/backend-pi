from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

from services import logic
from services.gpio_controller import gpio
from services.cache import (
    get_locker_id, set_rental_id, set_action, set_locker_id,
    get_available_slots, get_error
)
from services.config import settings

router = APIRouter()

class PerformRequest(BaseModel):
    action: Literal["DROP_OFF_BY_OWNER", "PICK_UP_BY_RENTER", "RETURN_BY_RENTER", "RETRIEVE_BY_OWNER"]
    rentalId: str
    lockerId: str

@router.post("/locker/perform")
def perform_locker_action(request: PerformRequest) -> dict:
    set_action(request.action)
    set_rental_id(request.rentalId)
    set_locker_id(request.lockerId)
    
    success = logic.perform_action()
    return {"success": success}

@router.get("/locker/closed")
def locker_closed_status():
    slot_id = get_locker_id()
    if not slot_id:
        print("[GPIO] No Slot is opened.")
        return {"closed": False}
    
    closed = gpio.is_slot_closed()
    if closed:
        gpio.close_slot(slot_id)
        print(f"[GPIO] Closed detected -> Lock completed: slot {slot_id}")
    else:
        print(f"[GPIO] Not closed yet: slot {slot_id}")

    return {"closed": closed}

class EmptySlotRequest(BaseModel):
    rentalId: str
    action: Literal["DROP_OFF_BY_OWNER", "RETURN_BY_RENTER"]

@router.post("/locker/empty")
def locker_empty_check_request(request: EmptySlotRequest):
    set_rental_id(request.rentalId)
    set_action(request.action)
    logic.get_empty_slot(request.rentalId, request.action)
    return { "success": True, "message": "빈 사물함 요청 전송됨"}

@router.get("/locker/empty/result")
def locker_empty_result():
    error = get_error()
    if error:
        return {
            "success": False,
            "message": error
        }
    
    slots = get_available_slots()
    if slots:
        return {
            "success": True,
            "data": {
                "lockers": [
                    {
                        "deviceId": settings.LOCKER_ID,
                        "lockerId": slot,
                        "available": True
                    } for slot in slots
                ]
            },
            "message": ""
        }
    return {
        "success": False,
        "message": "아직 빈 사물함 목록이 수신되지 않았습니다."
    }