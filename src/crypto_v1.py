import requests


# SETTINGS
url = 'https://api.coingecko.com/api/v3'


def get_price(coin, vs_currencies):
    endpoint = f'/simple/price?ids={coin}&vs_currencies={vs_currencies}'
    # REQUEST DATA
    data = requests.get(url + endpoint).json()
    result = data[coin]
    return result


if __name__ == '__main__':
    print('This is not main!')
    #print(get_price("pancakeswap-token", "usd,bnb"))
    #print(get_price("mdex", "usd,bnb"))
    