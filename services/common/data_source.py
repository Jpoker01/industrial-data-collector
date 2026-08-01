import logging
import requests
import json

logger = logging.getLogger(__name__)


COINBASE_URL = "https://api.coinbase.com/v2/prices/{pair}/spot"

def fetch_price(pair: str, timeout=5, fallback=None):
    url_to_fetch = COINBASE_URL.format(pair=pair)
    try:
        response = requests.get(url_to_fetch, timeout=timeout)
        response.raise_for_status
        amount = float(response.json()["data"]["amount"])
        return {"pair": pair, "price": amount, "source": "coinbase"}
    except (requests.RequestException, KeyError, ValueError) as exc:
        logger.warning("Price fetch failed (%s); using fallback", exc)
        return None





























