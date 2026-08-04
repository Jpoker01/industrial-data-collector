import logging
import os

logger = logging.getLogger(__name__)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TLS_CA = os.getenv("MQTT_TLS_CA")


def connect_to_broker(client, host, port):
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    if MQTT_TLS_CA:
        client.tls_set(ca_certs=MQTT_TLS_CA)
    try:
        client.connect(host, port, keepalive=60)
    except OSError as exc:
        logger.error("Could not reach broker: %s", exc)
        raise SystemExit(1)
