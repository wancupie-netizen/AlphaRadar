"""
AlphaRadar Token Query Service

Application Service responsible for retrieving
Token Detail payloads.

Responsibilities
----------------
- Load latest Intelligence Package
- Deserialize stored Intelligence
- Build Product Layer payload

This module does NOT:
- perform market analysis
- build DTOs
- access HTTP
- perform serialization
"""

from scanner.intelligence_store import (
    load_latest_intelligence,
)

from scanner.deserializers.intelligence_deserializer import (
    deserialize_package,
)


class TokenQueryService:
    """
    Application service responsible for
    building Token Detail payloads.
    """

    def get_token(
        self,
        symbol: str,
    ) -> dict | None:
        """
        Retrieve latest Token Detail payload.

        Parameters
        ----------
        symbol : str

        Returns
        -------
        dict | None
        """

        package = load_latest_intelligence(
            symbol.upper(),
        )

        if package is None:

            return None

        intelligence = deserialize_package(
            package,
        )

        return {

            "header": {

                "symbol":
                    intelligence["token"],

                "pair":
                    intelligence["decision"].metadata.pair,

                "chain":
                    intelligence["decision"].metadata.chain,

                "price":
                    None,

                "liquidity":
                    None,

                "volume_24h":
                    None,

                "market_cap":
                    None,

                "fdv":
                    None,

                "last_updated":
                    intelligence["decision"].metadata.timestamp,

            },

            "observation":
                intelligence["observation"],

            "signals":
                intelligence["signals"],

            "interpretations":
                intelligence["interpretations"],

            "decision":
                intelligence["decision"],

            "outcome":
                None,

            "learning":
                None,

            "knowledge":
                [],

        }