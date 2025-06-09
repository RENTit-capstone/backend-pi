import paho.mqtt.client as mqtt
import threading
import json

from services.config import settings

MQTT_BROKER = settings.MQTT_BROKER
MQTT_PORT = settings.MQTT_PORT
MQTT_KEEPALIVE = settings.MQTT_KEEPALIVE
MQTT_USERNAME = settings.MQTT_USERNAME
MQTT_PASSWORD = settings.MQTT_PASSWORD

mqtt_client = mqtt.Client()
callback_registry = {}


def on_connect(client, userdata, flags, rc) -> None:
    print(f"[MQTT] Connected with result code {rc}")
    for topic in callback_registry:
        client.subscribe(topic)


def on_message(client, userdata, msg) -> None:
    topic = msg.topic
    raw = msg.payload.decode("utf-8")

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print(f"[MQTT] Invalid JSON on {topic}: {raw}")
        return

    print(f"[MQTT] Message received on {topic}: {payload}")

    if topic in callback_registry:
        callback_registry[topic](payload)


def publish(topic: str, message: dict) -> None:
    try:
        json_message = json.dumps(message)
        print(f"[MQTT] Publishing to {topic}: {json_message}")
        mqtt_client.publish(topic, json_message, qos=1)
    except Exception as e:
        print(f"[MQTT] Failed to publish to {topic}: {e}")


def subscribe(topic: str, callback) -> None:
    print(f"[MQTT] Subscribing to {topic}")
    callback_registry[topic] = callback
    mqtt_client.subscribe(topic, qos=1)


def start() -> None:
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)

    thread = threading.Thread(target=mqtt_client.loop_forever, daemon=True)
    thread.start()
    print("[MQTT] Loop started in background")
