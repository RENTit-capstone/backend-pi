from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  MQTT_BROKER: str
  MQTT_PORT: int
  MQTT_KEEPALIVE: int = 60
  UNIVERSITY_ID: str
  LOCKER_ID: str

  class Config:
    env_file = ".env"
  
settings = Settings()