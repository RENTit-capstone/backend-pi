from fastapi import APIRouter
from services.cache import reset_slot_cache

router = APIRouter()

@router.post("/system/reset")
def reset_system_state():
    try:
        reset_slot_cache()
        return { "success": True }
    except Exception as e:
        print(f"[ERROR] Failed to reset system state: {e}")
        return { "success": False, "error": str(e) }