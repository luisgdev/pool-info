import requests


# SETTINGS
url = 'https://api.coingecko.com/api/v3'


def get_price(coin, vs_currencies):
    endpoint = f'/simple/price?ids={coin}&vs_currencies={vs_currencies}'
    # REQUEST DATA
    data = requests.get(url + endpoint).json()
    result = data[coin][vs_currencies]
    return result


def get_id(coin):
    data = get_coin_list()
    for item in data:
        if coin == item['symbol']:
            return item["id"]


def get_coin_list():
    endpoint = '/coins/list'
    # REQUEST DATA
    response = requests.get(url + endpoint).json()
    return response


if __name__ == '__main__':
    print('This is not main!')
    print(get_price("pancakeswap-token", "usd"))