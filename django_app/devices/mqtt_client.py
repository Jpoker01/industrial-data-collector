import os
import json

import paho.mqtt.client as mqtt

BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TLS_CA = os.getenv("MQTT_TLS_CA")

def publish_command(client_id, command):
    message = json.dumps({"command": command})
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    if MQTT_TLS_CA:
        client.tls_set(ca_certs=MQTT_TLS_CA)
    client.connect(BROKER_HOST, BROKER_PORT)
    client.loop_start()
    info = client.publish(f"commands/{client_id}", message, qos=1)
    info.wait_for_publish()
    client.loop_stop()
    client.disconnect()