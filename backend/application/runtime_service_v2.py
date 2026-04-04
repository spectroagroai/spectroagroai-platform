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

import gc


class RuntimeServiceV2:
    def predict(self, latitude, longitude, mode="baseline"):
        LocationValidator.validate(latitude, longitude)

        provider = OfflineCSVFeatureProvider()
        engine = InferenceEngine()
        domain = DomainAssessor()
        mode_engine = RuntimeModeEngine()
        unified_confidence = UnifiedConfidenceEngine()

        try:
            fv = provider.get_by_coordinates(latitude, longitude)

            if isinstance(fv.values, dict):
                feature_dict = fv.values
            else:
                feature_dict = {
                    name: fv.values[idx]
                    for idx, name in enumerate(engine.features)
                }

            result = engine.predict(feature_dict)

            domain_info = domain.assess(fv, result)
            result["domain"] = domain_info

            result["confidence"] = unified_confidence.compute(
                confidence=result["confidence"],
                domain=domain_info,
            )

            result = mode_engine.apply(result, mode=mode)

            result["metadata"] = result.get("metadata", {})
            result["metadata"]["requested_coordinates"] = fv.coordinates
            result["metadata"]["effective_coordinates"] = (
                fv.effective_coordinates
            )

            return result

        finally:
            del provider
            del engine
            del domain
            del mode_engine
            del unified_confidence

            gc.collect()