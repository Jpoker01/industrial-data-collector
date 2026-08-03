import os
import json

import paho.mqtt.client as mqtt

BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))


def publish_command(client_id, command, payload=None):
    message = json.dumps({"command": command, **(payload or {})})
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER_HOST, BROKER_PORT)
    client.loop_start()
    info = client.publish(f"commands/{client_id}", message, qos=1)
    info.wait_for_publish()
    client.loop_stop()
    client.disconnect()