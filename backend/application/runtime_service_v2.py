from backend.core.location_validator import LocationValidator
from backend.providers.offline.offline_csv_feature_provider import (
    OfflineCSVFeatureProvider,
)
from backend.inference.inference_engine import InferenceEngine
from backend.core.domain_assessor import DomainAssessor
from backend.core.runtime_mode_engine import RuntimeModeEngine
from backend.core.unified_confidence_engine import (
    UnifiedConfidenceEngine,
)


class RuntimeServiceV2:
    def __init__(self):
        self.provider = OfflineCSVFeatureProvider()
        self.engine = InferenceEngine()
        self.domain = DomainAssessor()
        self.mode_engine = RuntimeModeEngine()
        self.unified_confidence = UnifiedConfidenceEngine()

    def predict(self, latitude, longitude, mode="baseline"):
        LocationValidator.validate(latitude, longitude)

        fv = self.provider.get_by_coordinates(latitude, longitude)

        if isinstance(fv.values, dict):
            feature_dict = fv.values
        else:
            feature_dict = {
                name: fv.values[idx]
                for idx, name in enumerate(self.engine.features)
            }

        result = self.engine.predict(feature_dict)

        domain_info = self.domain.assess(fv, result)
        result["domain"] = domain_info

        result["confidence"] = self.unified_confidence.compute(
            confidence=result["confidence"],
            domain=domain_info,
        )

        result = self.mode_engine.apply(result, mode=mode)

        result["metadata"] = result.get("metadata", {})
        result["metadata"]["requested_coordinates"] = fv.coordinates
        result["metadata"]["effective_coordinates"] = (
            fv.effective_coordinates
        )

        return result