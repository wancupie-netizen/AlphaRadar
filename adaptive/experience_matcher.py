from __future__ import annotations

from experience_memory import (
    Experience,
    ExperienceMemory,
)


class ExperienceMatcher:
    """
    Finds historical experiences that match
    the current Market DNA.

    Current implementation:
        - Exact Market DNA matching

    Future versions may support:
        - Similarity search
        - Vector search
        - Hybrid ranking
        - Confidence weighting

    Public API is intentionally kept stable.
    """

    def __init__(
        self,
        memory: ExperienceMemory,
    ) -> None:

        self._memory = memory

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def match(
        self,
        market_dna: str,
        limit: int | None = None,
    ) -> list[Experience]:
        """
        Return experiences sharing the same Market DNA.

        Parameters
        ----------
        market_dna:
            Current Market DNA.

        limit:
            Optional maximum number of results.

        Returns
        -------
        list[Experience]
        """

        matches = self._memory.find_by_market_dna(
            market_dna
        )

        if limit is None:
            return matches

        return matches[:limit]

    def has_match(
        self,
        market_dna: str,
    ) -> bool:
        """
        True if at least one experience exists.
        """

        return (
            len(
                self._memory.find_by_market_dna(
                    market_dna
                )
            )
            > 0
        )

    def count(
        self,
        market_dna: str,
    ) -> int:
        """
        Number of matching experiences.
        """

        return len(
            self._memory.find_by_market_dna(
                market_dna
            )
        )