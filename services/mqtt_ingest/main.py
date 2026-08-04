import os
import json
import logging
from datetime import datetime, timezone

from pymongo import MongoClient
import paho.mqtt.client as mqtt

from common.broker import connect_to_broker

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "iot")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "mqtt_measurements")
TOPIC = os.getenv("TOPIC", "telemetry/#")

mongo = MongoClient(MONGO_URI)
collection = mongo[MONGO_DB][MONGO_COLLECTION]


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        logger.warning("Ignoring non-JSON message on %s", msg.topic)
        return
    document = {
        "source": "mqtt",
        "topic": msg.topic,
        "pair": payload.get("pair"),
        "price": payload.get("price"),
        "data_source": payload.get("source"),
        "received_at": datetime.now(timezone.utc),
        "raw": payload,
    }
    collection.insert_one(document)
    logger.info("Stored %s = %s", document["pair"], document["price"])


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="mqtt-ingest")
    client.on_message = on_message
    connect_to_broker(client, BROKER_HOST, BROKER_PORT)
    client.subscribe(TOPIC)
    client.loop_forever()


if __name__ == "__main__":
    main()
