import os 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MQTT_BROKER: str
    MQTT_PORT: int
    MQTT_KEEPALIVE: int = 60
    UNIVERSITY_ID: str
    LOCKER_ID: str
    SLOTS: list[str] = [""]

    USE_GPIO: bool = os.getenv("USE_GPIO", "False") == "True"

    model_config = {
        "env_file": "../.env"
    }

settings = Settings()

if settings.USE_GPIO:
    print("[ENV] Running in actual Pi...")
else:
    print("[ENV] Running in development environment...")
