from typing import List, Literal, Tuple

from pydantic import BaseModel


class PredictRequest(BaseModel):
    latitude: float
    longitude: float
    mode: Literal["baseline", "nowcast"] = "baseline"


class MetadataModel(BaseModel):
    manifest_version: str
    feature_count: int
    requested_coordinates: Tuple[float, float]
    effective_coordinates: Tuple[float, float]


class PredictionIntervalModel(BaseModel):
    mean: float
    lower: float
    upper: float
    width: float


class BDFIODPredictionModel(PredictionIntervalModel):
    sigma: float


class PredictionsModel(BaseModel):
    lab__CECPH7: PredictionIntervalModel
    lab__ORGC: PredictionIntervalModel
    lab__ORGM: PredictionIntervalModel
    lab__BDFIOD: BDFIODPredictionModel
    lab__TOTC: PredictionIntervalModel


class ConfidenceModel(BaseModel):
    score: float
    level: Literal["high", "medium", "low"]
    warning_count: int
    valid_feature_count: int
    base_score: float
    domain_support_score: float


class DomainModel(BaseModel):
    status: Literal[
        "supported",
        "borderline",
        "out_of_distribution",
    ]
    ood_score: float
    support_score: float
    distance_km: float
    valid_feature_count: int
    reasons: List[str]


class LSIModel(BaseModel):
    conservative: float
    expected: float
    opportunity: float


class PredictResponse(BaseModel):
    metadata: MetadataModel
    predictions: PredictionsModel
    warnings: List[str]
    confidence: ConfidenceModel
    lsi: LSIModel
    domain: DomainModel
    mode: Literal["baseline", "nowcast"]
    temporal_modifier: float
    temporal_confidence_penalty: float