import json
import os
import time
import logging

import paho.mqtt.client as mqtt

from common.data_source import fetch_price


logger = logging.getLogger(__name__)

#env variables
CLIENT_ID = os.getenv("CLIENT_ID", "pub-1")
BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))
PUBLISH_INTERVAL = int(os.getenv("PUBLISH_INTERVAL", "5"))
PAIR = os.getenv("PAIR", "BTC-USD")
TOPIC = f"telemetry/{CLIENT_ID}/crypto"

def connect_to_broker(client, host, port):
    try:
        client.connect(host, port, keepalive=60)
    except OSError as exc:
        logger.warning("Could not reach broker (%s)", exc)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
connect_to_broker(client, BROKER_HOST, BROKER_PORT)
client.loop_start()

try:
    while True:
        reading = fetch_price(PAIR)
        if reading is None:
            print("No data this cycle; skipping")
        else:
            message = json.dumps(reading)
            client.publish(TOPIC, message)
            print(f"Published: {message}")
        time.sleep(PUBLISH_INTERVAL)
except KeyboardInterrupt:
    print("Stopping")
finally:
    client.loop_stop()
    client.disconnect()