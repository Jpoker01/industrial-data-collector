import os
import time
import logging
import threading

from pymodbus.server import StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusSlaveContext,
    ModbusServerContext,
)

from pymodbus.client import ModbusTcpClient

from common.data_source import fetch_price

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

LISTEN_HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", "5020"))
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "5"))
PAIR = os.getenv("PAIR", "BTC-USD")


FLOAT32 = ModbusTcpClient.DATATYPE.FLOAT32

store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0] * 100))
context = ModbusServerContext(slaves=store, single=True)


def update_registers():
    counter = 0
    while True:
        reading = fetch_price(PAIR)
        if reading is not None:
            price_regs = ModbusTcpClient.convert_to_registers(reading["price"], FLOAT32)
            counter = (counter + 1) % 65536  # check if it fits in register
            store.setValues(
                3, 0, price_regs + [counter]
            )  # 3 = holding registers, 0 = starting adress
            logger.info(
                "Registers updated: price=%s counter=%s", reading["price"], counter
            )
        time.sleep(UPDATE_INTERVAL)


def main():
    # thread that updates registry values in UPDATE_INTERVAL
    # daemon=True - this thread gets killed if the main program is
    threading.Thread(target=update_registers, daemon=True).start()
    logger.info("Starting Modbus TCP server on %s:%s", LISTEN_HOST, LISTEN_PORT)
    StartTcpServer(
        context=context, address=(LISTEN_HOST, LISTEN_PORT)
    )  # main server that answers clients


if __name__ == "__main__":
    main()
