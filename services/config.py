from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MQTT_BROKER: str
    MQTT_PORT: int
    MQTT_KEEPALIVE: int = 60
    UNIVERSITY_ID: str
    LOCKER_ID: str
    SLOTS: list[str] = [""]

    model_config = {
        "env_file": "../.env"
    }

settings = Settings()
