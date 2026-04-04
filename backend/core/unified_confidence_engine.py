from __future__ import annotations

from typing import Any


class UnifiedConfidenceEngine:
    """
    SAFI v2 confidence synthesis engine.

    Combines:
    - existing ConfidenceEngine output
    - DomainAssessor support score
    """

    @staticmethod
    def compute(
        confidence: dict[str, Any],
        domain: dict[str, Any],
    ) -> dict[str, Any]:

        base_score = float(confidence.get("score", 1.0))
        support_score = float(domain.get("support_score", 1.0))

        # Soft domain weighting:
        # keeps confidence mostly intact for supported points
        # but significantly reduces it for OOD points
        final_score = base_score * (0.6 + 0.4 * support_score)

        final_score = max(0.0, min(1.0, final_score))

        if final_score >= 0.75:
            level = "high"
        elif final_score >= 0.45:
            level = "medium"
        else:
            level = "low"

        result = dict(confidence)

        result["base_score"] = round(base_score, 3)
        result["domain_support_score"] = round(support_score, 3)
        result["score"] = round(final_score, 3)
        result["level"] = level

        return result