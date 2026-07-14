from datetime import datetime


def normalize_pair(pair):
    return {
        "token": pair["baseToken"]["symbol"],
        "name": pair["baseToken"]["name"],
        "chain": pair["chainId"],
        "price": pair.get("priceUsd"),
        "liquidity": pair.get("liquidity", {}).get("usd"),
        "fdv": pair.get("fdv"),
        "market_cap": pair.get("marketCap"),
        "volume_24h": pair.get("volume", {}).get("h24"),
        "pair_address": pair.get("pairAddress"),
        "source": "DexScreener",
        "scanned_at": datetime.utcnow().isoformat()
    }