import requests

BASE_URL = "https://api.dexscreener.com/latest/dex/search"


def search_token(token_name: str):
    url = f"{BASE_URL}?q={token_name}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")

    return response.json()