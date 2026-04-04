from __future__ import annotations

from typing import Any


class LSIEngine:
    """
    SAFI v1 Land Suitability Index engine.

    Current implementation follows the locked SAFI logic:

    Positive drivers:
    - CECPH7
    - TOTC

    Constraint factors:
    - BDFIOD
    - ORGC / ORGM

    Produces:
    - conservative
    - expected
    - opportunity
    """

    @staticmethod
    def _normalize(
        value: float,
        lower_bound: float,
        upper_bound: float,
    ) -> float:
        """
        Normalize to [0, 1] with clipping.
        """

        if value <= lower_bound:
            return 0.0

        if value >= upper_bound:
            return 1.0

        return (value - lower_bound) / (upper_bound - lower_bound)

    @classmethod
    def compute(
        cls,
        predictions: dict[str, Any],
    ) -> dict[str, float]:
        """
        predictions must contain:
        - lab__CECPH7
        - lab__TOTC
        - lab__ORGC
        - lab__ORGM
        - lab__BDFIOD
        """

        # Positive suitability drivers
        cec = predictions["lab__CECPH7"]
        totc = predictions["lab__TOTC"]

        # Constraint variables
        orgm = predictions["lab__ORGM"]
        bdf = predictions["lab__BDFIOD"]

        # Conservative case: pessimistic view
        conservative_driver = (
            cls._normalize(cec["lower"], 0, 40)
            + cls._normalize(totc["lower"], 0, 10)
        ) / 2.0

        conservative_constraint = (
            cls._normalize(orgm["lower"], 0, 15)
            * (1.0 - cls._normalize(bdf["upper"], 1.0, 2.0))
        )

        conservative = conservative_driver * conservative_constraint

        # Expected case: central estimate
        expected_driver = (
            cls._normalize(cec["mean"], 0, 40)
            + cls._normalize(totc["mean"], 0, 10)
        ) / 2.0

        expected_constraint = (
            cls._normalize(orgm["mean"], 0, 15)
            * (1.0 - cls._normalize(bdf["mean"], 1.0, 2.0))
        )

        expected = expected_driver * expected_constraint

        # Opportunity case: optimistic interpretation
        opportunity_driver = (
            cls._normalize(cec["upper"], 0, 40)
            + cls._normalize(totc["upper"], 0, 10)
        ) / 2.0

        opportunity_constraint = (
            cls._normalize(orgm["upper"], 0, 15)
            * (1.0 - cls._normalize(bdf["lower"], 1.0, 2.0))
        )

        opportunity = opportunity_driver * opportunity_constraint

        return {
            "conservative": round(float(conservative), 3),
            "expected": round(float(expected), 3),
            "opportunity": round(float(opportunity), 3),
        }