"""
Common MQTT broker connection utilities
"""

import logging
import os

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TLS_CA = os.getenv("MQTT_TLS_CA", "/certs/ca.crt")


def connect_to_broker(client: mqtt.Client, host: str, port: int) -> None:
    """
    Configures authentication to Mosquitto broker, TLS authentication and establishes connection
    Args:
        client: paho-MQTT client instance
        host: Hostname of the broker to connect to
        port: Port of the broker to connect to
    """
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    if MQTT_TLS_CA:
        client.tls_set(ca_certs=MQTT_TLS_CA)

    try:
        client.connect(host, port, keepalive=60)
    except OSError as exc:
        logger.error("Could not reach broker: %s", exc)
        raise SystemExit(1) from exc
