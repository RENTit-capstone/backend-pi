import paho.mqtt.client as mqtt
import threading
import json

from services.config import settings

MQTT_BROKER = settings.MQTT_BROKER
MQTT_PORT = settings.MQTT_PORT
MQTT_KEEPALIVE = settings.MQTT_KEEPALIVE

mqtt_client = mqtt.Client()

callback_registry = {}

def on_connect(client, userdata, flags, rc):
  print(f"[MQTT] Connected with result code {rc}")
  for topic in callback_registry:
    client.subscribe(topic)

def on_message(client, userdata, msg):
  topic = msg.topic
  payload_raw = msg.payload.decode("utf-8")
  
  try:
    payload = json.loads(payload_raw)
  except json.JSONDecodeError:
    print(f"[MQTT] Invalid JSON format on {topic}: {payload_raw}")
    return
  
  print(f"[MQTT] Message received on {topic}: {payload}")

  if topic in callback_registry:
    callback_registry[topic](payload)

def publish(topic: str, message: dict):
  try:
    json_message = json.dumps(message)
    print(f"[MQTT] Publishing to {topic}: {json_message}")
    mqtt_client.publish(topic, json_message)
  except Exception as e:
    print(f"[MQTT] Failed to publish to {topic}: {e}")

def subscribe(topic: str, callback):
  print(f"[MQTT] Subscribing to {topic}")
  callback_registry[topic] = callback
  mqtt_client.subscribe(topic)

def start():
  mqtt_client.on_connect = on_connect
  mqtt_client.on_message = on_message

  mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)

  thread = threading.Thread(target=mqtt_client.loop_forever, daemon=True)
  thread.start()
  print(f"[MQTT] Loop started in background")
