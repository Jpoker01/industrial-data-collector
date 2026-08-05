"""Data source module for fetching Coinbase price data"""

import logging

import requests

logger = logging.getLogger(__name__)


COINBASE_URL = "https://api.coinbase.com/v2/prices/{pair}/spot"


def fetch_price(pair: str, timeout: int = 5, fallback=None) -> dict | None:
    """
    Fetches price for a given currency pair from free Coinbase API

    Args:
        pair: Chosen pair string in the format "BTC-USD"
        timeout: Request time out in seconsd
        fallback: What to return if request fails

    Returns:
        Dictionary containing pair, price amount, source of the data OR None if request fails
    """
    url_to_fetch = COINBASE_URL.format(pair=pair)
    try:
        response = requests.get(url_to_fetch, timeout=timeout)
        response.raise_for_status()
        amount = float(response.json()["data"]["amount"])
        return {"pair": pair, "price": amount, "source": "coinbase"}
    except (requests.RequestException, KeyError, ValueError) as exc:
        logger.warning("Price fetch failed %s (%s); using fallback", pair, exc)
        return fallback
