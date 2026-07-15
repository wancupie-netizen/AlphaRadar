from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class MarketSnapshot:
    """
    Immutable representation of a normalized market state.

    This model is the official boundary between the Infrastructure
    Layer and the Intelligence Layer.

    Responsibilities
    ----------------
    - Represent market facts only.
    - Contain no business logic.
    - Contain no market analysis.
    - Remain provider-independent.
    """

    symbol: str

    pair: str

    chain: str

    price: Decimal

    liquidity: Decimal

    volume_24h: Decimal

    fdv: Optional[Decimal] = None

    market_cap: Optional[Decimal] = None

    buyers_24h: Optional[int] = None

    sellers_24h: Optional[int] = None

    transactions_24h: Optional[int] = None

    provider: str = "Unknown"

    captured_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    snapshot_id: str = field(
        default_factory=lambda: f"SNP-{uuid4().hex[:12].upper()}"
    )