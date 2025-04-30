import paho.mqtt.client as mqtt
import threading

from services.config import settings

MQTT_BROKER = settings.MQTT_BROKER
MQTT_PORT = settings.MQTT_PORT
MQTT_KEEPALIVE = settings.MQTT_KEEPALIVE

client = mqtt.Client()

callback_registry = {}

def on_connect(client, userdata, flags, rc):
  pass

def on_message(client, userdata, msg):
  pass

def publish(topic: str, message: str):
  pass

def subscribe(topic: str, callback):
  pass

def start():
  pass
