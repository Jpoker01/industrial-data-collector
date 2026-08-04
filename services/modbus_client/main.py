import os
import time
import logging
from datetime import datetime, timezone

from pymodbus.client import ModbusTcpClient
from pymongo import MongoClient

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

MODBUS_HOST = os.getenv("MODBUS_HOST", "localhost")
MODBUS_PORT = int(os.getenv("MODBUS_PORT", "5020"))
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "iot")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "modbus_measurements")

FLOAT32 = ModbusTcpClient.DATATYPE.FLOAT32

mongo = MongoClient(MONGO_URI)
collection = mongo[MONGO_DB][MONGO_COLLECTION]


def connect_to_server(client):
    if not client.connect():
        logger.error("Could not reach Modbus server")
        raise SystemExit(1)


def main():
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    connect_to_server(client)
    try:
        while True:
            # first two registers hold the price value,
            # the third is a counter that is used to check whether the server is updating the first two values
            result = client.read_holding_registers(0, count=3)
            if result.isError():
                logger.warning("Read error: %s", result)
            else:
                price = client.convert_from_registers(result.registers[0:2], FLOAT32)
                counter = result.registers[2]
                document = {
                    "source": "modbus",
                    "registers": result.registers,
                    "price": price,
                    "counter": counter,
                    "received_at": datetime.now(timezone.utc),
                }
                collection.insert_one(document)
                logger.info("Stored price=%s counter=%s", price, counter)
            time.sleep(POLL_INTERVAL)
    finally:
        client.close()


if __name__ == "__main__":
    main()
