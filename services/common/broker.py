import logging

logger = logging.getLogger(__name__)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

def connect_to_broker(client, host, port):
    try:
        client.connect(host, port, keepalive=60)
    except OSError as exc:
        logger.error("Could not reach broker: %s", exc)
        raise SystemExit(1)