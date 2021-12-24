from typing import Dict
import requests


# SETTINGS
url: str = "https://api.coingecko.com/api/v3"


def get_price(symbol: str, vs_pairs: str = "usd") -> Dict[str, float]:
    endpoint: str = f"/simple/price?ids={symbol}&vs_currencies={vs_pairs}"
    # REQUEST DATA
    data: dict = requests.get(url + endpoint).json()
    result: Dict[str, float] = data[symbol]
    return result


if __name__ == "__main__":
    print("This is not main!")
    # print(get_price("pancakeswap-token", "usd,bnb"))
