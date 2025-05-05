from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

from services import logic
from services.gpio_controller import gpio

router = APIRouter()

class PerformRequest(BaseModel):
    action: Literal["store", "borrow", "return", "retrieve"]
    item: dict
    slot: str

@router.post("/locker/perform")
def perform_locker_action(request: PerformRequest) -> dict:
    success = logic.perform_action(
        item=request.item,
        slot_id=request.slot,
        action=request.action
    )

    return {"success": success}

@router.get("/locker/closed")
def locker_closed_status():
    closed = gpio.is_slot_closed()
    return {"closed": closed}
