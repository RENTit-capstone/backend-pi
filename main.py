from services import mqtt_client
import time

def handle_test_message(payload):
  print(f"[TEST] Callback triggered with payload: {payload}")

def main():
  print("[TEST] Starting MQTT client...")
  mqtt_client.subscribe("test/topic", handle_test_message)
  mqtt_client.start()

  time.sleep(2)
  mqtt_client.publish("test/topic", {
    "message": "Hello from test",
    "timestamp": "2025-04-30T12:34:56"
  })

  time.sleep(5)
  print("[TEST] Done.")

if __name__ == "__main__":
  main()