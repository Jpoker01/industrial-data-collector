import json
import os
import time
import logging

import paho.mqtt.client as mqtt

from common.data_source import fetch_price
from common.broker import connect_to_broker

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("CLIENT_ID", "pub-1")
BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))
PUBLISH_INTERVAL = int(os.getenv("PUBLISH_INTERVAL", "5"))
PAIR = os.getenv("PAIR", "BTC-USD")

TOPIC = f"telemetry/{CLIENT_ID}/crypto"
COMMAND_TOPIC = f"commands/{CLIENT_ID}"

publishing_enabled = True

def on_message(client, userdata, msg):
    global publishing_enabled
    try:
        command = json.loads(msg.payload.decode()).get("command")
    except json.JSONDecodeError:
        logger.warning("Ignoring non-JSON command: %s", msg.payload)
        return
    if command == "stop":
        publishing_enabled = False
        logger.info("STOP received; pausing")
    elif command == "start":
        publishing_enabled = True
        logger.info("START received; resuming")
    else:
        logger.warning("Unknown command: %s", command)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.on_message = on_message
    connect_to_broker(client, BROKER_HOST, BROKER_PORT)

    connect_to_broker(client, BROKER_HOST, BROKER_PORT)
    client.subscribe(COMMAND_TOPIC)
    client.loop_start()

    try:
        while True:
            if publishing_enabled:
                reading = fetch_price(PAIR)
                if reading is None:
                    logger.info("No data this cycle; skipping")
                else:
                    payload = json.dumps(reading)
                    client.publish(TOPIC, payload)
                    logger.info("Published: %s", payload)
            time.sleep(PUBLISH_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Stopping")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
    