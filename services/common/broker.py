import logging

logger = logging.getLogger(__name__)

def connect_to_broker(client, host, port):
    try:
        client.connect(host, port, keepalive=60)
    except OSError as exc:
        logger.error("Could not reach broker: %s", exc)
        raise SystemExit(1)