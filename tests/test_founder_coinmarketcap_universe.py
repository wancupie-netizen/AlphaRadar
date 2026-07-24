"""
Tests for CoinMarketCap Top 100 Universe.
"""

import json
from datetime import (
    datetime,
    timedelta,
    timezone,
)

import pytest

from application.coinmarketcap_universe import (
    COINMARKETCAP_LISTINGS_URL,
    fetch_coinmarketcap_top_100,
    load_top_100_universe,
    read_cached_universe,
)


class FakeResponse:
    """
    Minimal successful HTTP response.
    """

    def __init__(
        self,
        payload,
    ):
        self._payload = payload

    def raise_for_status(
        self,
    ) -> None:
        return None

    def json(
        self,
    ):
        return self._payload


def test_should_fetch_ranked_top_100_symbols(
    tmp_path,
):
    """
    CoinMarketCap ordering should be preserved.
    """

    calls: list[dict[str, object]] = []

    payload = {
        "data": [
            {
                "symbol": "BTC",
            },
            {
                "symbol": "ETH",
            },
            {
                "symbol": "SOL",
            },
        ]
    }

    def fake_get(
        url,
        *,
        headers,
        params,
        timeout,
    ):
        calls.append(
            {
                "url": url,
                "headers": headers,
                "params": params,
                "timeout": timeout,
            }
        )

        return FakeResponse(
            payload,
        )

    cache_file = (
        tmp_path
        / "top100.json"
    )

    tokens = fetch_coinmarketcap_top_100(
        api_key="test-key",
        get=fake_get,
        cache_file=cache_file,
    )

    assert tokens == (
        "BTC",
        "ETH",
        "SOL",
    )

    assert calls[0]["url"] == (
        COINMARKETCAP_LISTINGS_URL
    )

    assert calls[0]["headers"][
        "X-CMC_PRO_API_KEY"
    ] == "test-key"

    assert calls[0]["params"] == {
        "start": 1,
        "limit": 100,
        "convert": "USD",
    }

    assert calls[0]["timeout"] == 20

    assert cache_file.exists()


def test_should_use_fresh_daily_cache(
    tmp_path,
):
    """
    Fresh cache should avoid another API request.
    """

    now = datetime(
        2026,
        7,
        24,
        8,
        0,
        tzinfo=timezone.utc,
    )

    cache_file = (
        tmp_path
        / "top100.json"
    )

    cache_file.write_text(
        json.dumps(
            {
                "fetched_at": (
                    now
                    - timedelta(
                        hours=2,
                    )
                ).isoformat(),
                "tokens": [
                    "BTC",
                    "ETH",
                ],
            }
        ),
        encoding="utf-8",
    )

    def failing_get(
        *args,
        **kwargs,
    ):
        raise AssertionError(
            "API should not be called."
        )

    tokens = load_top_100_universe(
        cache_file=cache_file,
        now=now,
        get=failing_get,
    )

    assert tokens == (
        "BTC",
        "ETH",
    )


def test_should_reject_expired_cache(
    tmp_path,
):
    """
    Cache older than twenty-four hours is stale.
    """

    now = datetime(
        2026,
        7,
        24,
        8,
        0,
        tzinfo=timezone.utc,
    )

    cache_file = (
        tmp_path
        / "top100.json"
    )

    cache_file.write_text(
        json.dumps(
            {
                "fetched_at": (
                    now
                    - timedelta(
                        hours=25,
                    )
                ).isoformat(),
                "tokens": [
                    "BTC",
                ],
            }
        ),
        encoding="utf-8",
    )

    assert read_cached_universe(
        cache_file=cache_file,
        now=now,
    ) is None


def test_should_reject_missing_api_key(
    tmp_path,
    monkeypatch,
):
    """
    API key is required when no cache exists.
    """

    monkeypatch.delenv(
        "COINMARKETCAP_API_KEY",
        raising=False,
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "COINMARKETCAP_API_KEY is not configured"
        ),
    ):

        load_top_100_universe(
            cache_file=(
                tmp_path
                / "missing.json"
            ),
            api_key="",
        )