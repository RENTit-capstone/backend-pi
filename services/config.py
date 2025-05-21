import os 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MQTT_BROKER: str
    MQTT_PORT: int
    MQTT_KEEPALIVE: int = 60
    MQTT_USERNAME: str
    MQTT_PASSWORD: str
    LOCKER_ID: str
    SLOTS: list[str] = [""]

    USE_GPIO: bool = os.getenv("USE_GPIO", "False") == "True"

    model_config = {
        "env_file": os.path.join(os.path.dirname(__file__), "..", ".env")
    }

settings = Settings()

if settings.USE_GPIO:
    print("[ENV] Running in actual Pi...")
else:
    print("[ENV] Running in development environment...")

print(f"[ENV] Loaded LOCKER_ID = {settings.LOCKER_ID}")
