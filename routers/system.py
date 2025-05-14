from fastapi import APIRouter
from services.cache import wipe_state

router = APIRouter()

@router.post("/system/reset")
def reset_system_state():
    try:
        wipe_state()
        return { "success": True }
    except Exception as e:
        print(f"[ERROR] Failed to reset system state: {e}")
        return {
            "success": False,
            "error": str(e)
        }
