from __future__ import annotations

from typing import Any


class ConfidenceEngine:
    """
    SAFI confidence synthesis engine.

    Combines:
    - prediction interval width
    - valid feature count
    - physical consistency warnings
    """

    @staticmethod
    def compute(
        predictions: dict[str, Any],
        valid_feature_count: int,
        warnings: list[str],
    ) -> dict[str, Any]:

        widths = [
            predictions["lab__CECPH7"]["width"],
            predictions["lab__TOTC"]["width"],
            predictions["lab__ORGC"]["width"],
            predictions["lab__BDFIOD"]["width"],
        ]

        avg_width = sum(widths) / len(widths)

        confidence_score = 1.0

        # Penalize wide prediction intervals
        if avg_width > 10:
            confidence_score -= 0.35
        elif avg_width > 5:
            confidence_score -= 0.20

        # Penalize missing features
        if valid_feature_count < 157:
            missing_fraction = 1.0 - (valid_feature_count / 157.0)
            confidence_score -= 0.5 * missing_fraction

        # Penalize physical consistency warnings
        confidence_score -= 0.15 * len(warnings)

        confidence_score = max(0.0, min(1.0, confidence_score))

        if confidence_score >= 0.75:
            level = "high"
        elif confidence_score >= 0.45:
            level = "medium"
        else:
            level = "low"

        return {
            "score": round(confidence_score, 3),
            "level": level,
            "warning_count": len(warnings),
            "valid_feature_count": valid_feature_count,
        }
