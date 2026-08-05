"""
MQTT CLIENT for sending commands from DjangoAPI to other publishing clients
"""

import json
import os

import paho.mqtt.client as mqtt

BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TLS_CA = os.getenv("MQTT_TLS_CA")


def publish_command(client_id: int, command: str) -> None:
    """
    Publishes JSON command to 'commands/{client_id}' topic

    Args:
        client-id: target MQTT client
        command: command string
    """

    message = json.dumps({"command": command})
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    if MQTT_TLS_CA:
        client.tls_set(ca_certs=MQTT_TLS_CA)

    client.connect(BROKER_HOST, BROKER_PORT)
    client.loop_start()
    try:
        info = client.publish(f"commands/{client_id}", message, qos=1)
        info.wait_for_publish()
    finally:
        client.loop_stop()
        client.disconnect()
