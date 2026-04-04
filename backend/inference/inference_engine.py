from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from backend.core.confidence_engine import ConfidenceEngine
from backend.core.consistency_validator import ConsistencyValidator
from backend.core.lsi_engine import LSIEngine
from backend.inference.domain_validator import DomainValidator
from backend.inference.model_registry import ModelRegistry
from backend.inference.uncertainty_engine import UncertaintyEngine
from backend.providers.feature_vector import FeatureVector


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "config" / "safi_covariate_manifest_v5.json"


class InferenceEngine:
    def __init__(self):
        self.registry = ModelRegistry()
        self.features = self._load_manifest_features()

    def _load_manifest_features(self) -> list[str]:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        features = [item["feature_id"] for item in manifest["features"]]

        if len(features) != 157:
            raise RuntimeError(
                f"Manifest v5 must contain 157 features, found {len(features)}"
            )

        return features

    def _normalize_input(
        self,
        feature_input: dict[str, Any] | FeatureVector,
    ) -> dict[str, Any]:
        """
        Accept either:
        - raw SAFI feature dict
        - FeatureVector from any provider

        Always return canonical feature dictionary in exact manifest order.
        """

        if isinstance(feature_input, FeatureVector):
            if len(feature_input.values) != len(self.features):
                raise ValueError(
                    f"FeatureVector contains {len(feature_input.values)} values "
                    f"but manifest requires {len(self.features)}"
                )

            return {
                feature_name: feature_input.values[idx]
                for idx, feature_name in enumerate(self.features)
            }

        return {
            feature_name: feature_input.get(feature_name)
            for feature_name in self.features
        }

    def _build_dataframe(
        self,
        feature_values: dict[str, Any],
    ) -> pd.DataFrame:
        missing = [f for f in self.features if f not in feature_values]
        extra = [f for f in feature_values if f not in self.features]

        if missing:
            raise ValueError(
                "Missing required SAFI features:\n" + "\n".join(missing)
            )

        if extra:
            raise ValueError(
                "Unexpected extra features:\n" + "\n".join(extra)
            )

        row = {
            feature: feature_values[feature]
            for feature in self.features
        }

        return pd.DataFrame([row], columns=self.features)

    def predict(
        self,
        feature_input: dict[str, Any] | FeatureVector,
    ) -> dict[str, Any]:
        feature_values = self._normalize_input(feature_input)

        X = self._build_dataframe(feature_values)

        errors = DomainValidator.validate(feature_values)

        if errors:
            raise ValueError(
                "Domain validation failed:\n" + "\n".join(errors)
            )

        # CECPH7
        cec_p10 = self.registry.predict("lab__CECPH7", "p10", X)[0]
        cec_p50 = self.registry.predict("lab__CECPH7", "p50", X)[0]
        cec_p90 = self.registry.predict("lab__CECPH7", "p90", X)[0]

        # ORGC
        orgc_mu = self.registry.predict("lab__ORGC", "mu", X)[0]

        # Placeholder interval until Mondrian calibration is connected
        orgc_lower = orgc_mu - 1.0
        orgc_upper = orgc_mu + 1.5

        # ORGM derived deterministically from ORGC
        orgm_mu = orgc_mu * 1.724
        orgm_lower = orgc_lower * 1.724
        orgm_upper = orgc_upper * 1.724

        # BDFIOD
        bdf_mu = self.registry.predict("lab__BDFIOD", "mu", X)[0]
        bdf_sigma = self.registry.predict("lab__BDFIOD", "sigma", X)[0]

        # TOTC
        totc_q05 = self.registry.predict("lab__TOTC", "global_q05", X)[0]
        totc_q50 = self.registry.predict("lab__TOTC", "global_q50", X)[0]
        totc_q95 = self.registry.predict("lab__TOTC", "global_q95", X)[0]

        metadata = {
            "manifest_version": "safi_covariate_v5",
            "feature_count": len(self.features),
        }

        if isinstance(feature_input, FeatureVector):
            metadata.update(
                {
                    "source": feature_input.source,
                    "coordinates": feature_input.coordinates,
                    "effective_coordinates": feature_input.effective_coordinates,
                    "valid_feature_count": sum(
                        1 for v in feature_input.validity_mask.values() if v
                    ),
                }
            )

            if feature_input.metadata:
                metadata["provider_metadata"] = feature_input.metadata

        predictions = {
            "lab__CECPH7": UncertaintyEngine.cecph7(
                cec_p10,
                cec_p50,
                cec_p90,
            ),
            "lab__ORGC": {
                "mean": float(orgc_mu),
                "lower": float(orgc_lower),
                "upper": float(orgc_upper),
                "width": float(orgc_upper - orgc_lower),
            },
            "lab__ORGM": {
                "mean": float(orgm_mu),
                "lower": float(orgm_lower),
                "upper": float(orgm_upper),
                "width": float(orgm_upper - orgm_lower),
            },
            "lab__BDFIOD": UncertaintyEngine.bdfiod(
                bdf_mu,
                bdf_sigma,
            ),
            "lab__TOTC": UncertaintyEngine.totc(
                totc_q05,
                totc_q50,
                totc_q95,
            ),
        }

        warnings = ConsistencyValidator.validate(predictions)

        valid_feature_count = metadata.get(
            "valid_feature_count",
            len(self.features),
        )

        confidence = ConfidenceEngine.compute(
            predictions=predictions,
            valid_feature_count=valid_feature_count,
            warnings=warnings,
        )

        lsi = LSIEngine.compute(predictions)

        return {
            "metadata": metadata,
            "predictions": predictions,
            "warnings": warnings,
            "confidence": confidence,
            "lsi": lsi,
        }

    def predict_batch(
        self,
        rows: list[dict[str, Any] | FeatureVector],
    ) -> list[dict[str, Any]]:
        return [self.predict(row) for row in rows]


if __name__ == "__main__":
    engine = InferenceEngine()

    dummy = {feature: 0.0 for feature in engine.features}

    result = engine.predict(dummy)

    import pprint

    pprint.pprint(result)
