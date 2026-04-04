from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class FeatureVector:
    values: dict[str, float]
    validity_mask: dict[str, bool]
    coordinates: tuple[float, float]
    effective_coordinates: tuple[float, float]
    source: str
    metadata: Optional[dict] = None