CHAIN_PRIORITY = [
    "ethereum",
    "solana",
    "base",
    "bsc",
    "sui",
    "arbitrum",
    "polygon",
    "avalanche",
    "tron"
]


def select_best_pair(pairs):

    if not pairs:
        return None

    for chain in CHAIN_PRIORITY:

        candidates = [
            pair
            for pair in pairs
            if pair.get("chainId", "").lower() == chain
        ]

        if candidates:
            candidates.sort(
                key=lambda x: x.get("liquidity", {}).get("usd", 0),
                reverse=True
            )

            return candidates[0]

    return pairs[0]