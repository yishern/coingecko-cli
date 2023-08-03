import requests

URL_TEMPLATE = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={per_page}&page={page}&sparkline=true&price_change_percentage=1h%2C24h%2C7d"

def get_market_data(page: int, per_page: int):
    r = requests.get(URL_TEMPLATE.format(page=page, per_page=per_page), timeout=10)
    return r.json()