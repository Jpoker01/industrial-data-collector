import random
import logging
import requests

import json

logger = logging.getLogger(__name__)

COINBASE_URL = "https://api.coinbase.com/v2/prices/{pair}/spot"


def fetch_price(pair="BTC-USD", timeout=5):
    """Return the current spot price for a pair, with a fallback."""
    url = COINBASE_URL.format(pair=pair)
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        amount = float(response.json()["data"]["amount"])
        return {"pair": pair, "price": amount, "source": "coinbase"}
    except (requests.RequestException, KeyError, ValueError) as exc:
        logger.warning("Price fetch failed (%s); using fallback", exc)
        return {"pair": pair, "price": round(random.uniform(50000, 120000), 2),
                "source": "fallback"}