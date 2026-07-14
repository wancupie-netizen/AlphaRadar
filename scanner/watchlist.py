import json


def load_watchlist():

    with open("config/watchlist.json", "r") as file:
        data = json.load(file)

    return data["tokens"]