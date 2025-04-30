from pydantic import BaseSettings

class Settings(BaseSettings):
  MQTT_BROKER: str
  MQTT_PORT: int
  MQTT_KEEPALIVE: int = 60

  class Config:
    env_file = ".env"
  
settings = Settings()