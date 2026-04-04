class RuntimeModeEngine:
    """
    Adds Baseline / Now-Cast runtime behavior
    without modifying the existing SAFI runtime.
    """

    def apply(self, result: dict, mode: str = "baseline") -> dict:
        output = dict(result)

        if mode == "baseline":
            output["mode"] = "baseline"
            output["temporal_modifier"] = 0.0
            output["temporal_confidence_penalty"] = 0.0
            return output

        if mode == "nowcast":
            confidence = output.get("confidence", {})
            current_score = confidence.get("score", 1.0)

            # placeholder penalty for future temporal drift logic
            temporal_penalty = 0.15

            adjusted_score = max(0.0, current_score - temporal_penalty)

            if adjusted_score >= 0.80:
                level = "high"
            elif adjusted_score >= 0.50:
                level = "medium"
            else:
                level = "low"

            output["mode"] = "nowcast"
            output["temporal_modifier"] = -0.10
            output["temporal_confidence_penalty"] = temporal_penalty

            output["confidence"] = dict(confidence)
            output["confidence"]["score"] = round(adjusted_score, 3)
            output["confidence"]["level"] = level

            return output

        raise ValueError(f"Unsupported mode: {mode}")