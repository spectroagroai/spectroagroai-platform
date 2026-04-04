from math import radians, sin, cos, sqrt, atan2


class DomainAssessor:
    """
    Lightweight post-inference domain assessment layer.

    Uses only existing FeatureVector metadata and inference outputs.
    Does not modify the current SAFI runtime.
    """

    def __init__(
        self,
        max_supported_distance_km: float = 100.0,
    ):
        self.max_supported_distance_km = max_supported_distance_km

    @staticmethod
    def haversine_km(lat1, lon1, lat2, lon2):
        R = 6371.0

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = (
            sin(dlat / 2) ** 2
            + cos(radians(lat1))
            * cos(radians(lat2))
            * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def assess(self, feature_vector, inference_result):
        requested = feature_vector.coordinates
        effective = feature_vector.effective_coordinates

        distance_km = self.haversine_km(
            requested[0],
            requested[1],
            effective[0],
            effective[1],
        )

        if isinstance(feature_vector.validity_mask, dict):
            valid_feature_count = sum(
                1 for v in feature_vector.validity_mask.values() if v
            )
        else:
            valid_feature_count = int(feature_vector.validity_mask.sum())
        warning_count = len(inference_result.get("warnings", []))

        reasons = []

        if distance_km > 100:
            reasons.append(
                f"Nearest SAFI reference point is far away ({distance_km:.1f} km)"
            )

        if valid_feature_count < 140:
            reasons.append(
                f"Only {valid_feature_count}/157 features are valid"
            )

        if warning_count > 0:
            reasons.append(
                f"{warning_count} physical consistency warning(s) detected"
            )

        # Penalty scoring
        score = 1.0

        if distance_km > 5:
            score -= 0.10
        if distance_km > 25:
            score -= 0.20
        if distance_km > 100:
            score -= 0.30

        if valid_feature_count < 157:
            score -= (157 - valid_feature_count) / 157.0

        if warning_count > 0:
            score -= min(0.20, warning_count * 0.05)

        score = max(0.0, min(1.0, score))

        if score >= 0.80:
            status = "supported"
        elif score >= 0.50:
            status = "borderline"
        else:
            status = "out_of_distribution"

        return {
            "status": status,
            "ood_score": round(1.0 - score, 3),
            "support_score": round(score, 3),
            "distance_km": round(distance_km, 2),
            "valid_feature_count": valid_feature_count,
            "reasons": reasons,
        }