from typing import Dict
import requests


# SETTINGS
URL: str = "https://api.coingecko.com/api/v3"
SIMPLE_PRICE: str = "/simple/price"


def get_price(symbol: str, vs_pairs: str = "usd") -> Dict[str, float]:
    """
    Get price from Coingecko.
    :param symbol: Cryptocurrency symbol.
    :param vs_pairs: Pair to get price.
    :return: Dict with the price information.
    """
    params: Dict[str, str] = {"ids": symbol, "vs_currencies": vs_pairs}
    data: dict = requests.get(url=URL + SIMPLE_PRICE, params=params).json()
    result: Dict[str, float] = data[symbol]
    return result


if __name__ == "__main__":
    print("This is not main!")

