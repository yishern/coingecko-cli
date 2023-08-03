import requests

URL_TEMPLATE = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={per_page}&page={page}&sparkline=true&price_change_percentage=1h%2C24h%2C7d"

COINGECKO_TOKEN_URLS = {
    "token_info": "https://api.coingecko.com/api/v3/coins/{token_id}",
    "token_market_chart": "https://api.coingecko.com/api/v3/coins/{token_id}/market_chart?vs_currency=usd&days={days}"
}

def get_market_data(page: int, per_page: int):
    r = requests.get(URL_TEMPLATE.format(page=page, per_page=per_page), timeout=10)
    return r.json()

def get_token_data(token_id: str, days: int):
    token_info = requests.get(COINGECKO_TOKEN_URLS["token_info"].format(token_id=token_id, days=days), timeout=10).json()
    market_chart = requests.get(COINGECKO_TOKEN_URLS["token_market_chart"].format(token_id=token_id, days=days), timeout=10).json()
    return {"token_info": token_info, "market_chart": market_chart}