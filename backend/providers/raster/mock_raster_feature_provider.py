from pathlib import Path
import json

import numpy as np
import pandas as pd

from backend.providers.base_feature_provider import BaseFeatureProvider
from backend.providers.feature_vector import FeatureVector


PROJECT_ROOT = Path(__file__).resolve().parents[3]

CSV_PATH = PROJECT_ROOT / "artifacts/reference/safi_v1_universe.csv"
MAPPING_PATH = PROJECT_ROOT / "config/raster_feature_mapping.json"


class MockRasterFeatureProvider(BaseFeatureProvider):

    def __init__(self):
        if not CSV_PATH.exists():
            raise FileNotFoundError(f"Missing CSV: {CSV_PATH}")

        if not MAPPING_PATH.exists():
            raise FileNotFoundError(f"Missing mapping: {MAPPING_PATH}")

        self.df = pd.read_csv(CSV_PATH)

        with open(MAPPING_PATH, "r", encoding="utf-8") as f:
            mapping = json.load(f)

        self.features = [
            item["feature_name"]
            for item in mapping["features"]
        ]

        if len(self.features) != 157:
            raise ValueError(
                f"Expected 157 mapped features, got {len(self.features)}"
            )

    def _row_to_feature_vector(self, row, metadata):
        values = []
        validity_mask = []

        for feature_name in self.features:
            value = row.get(feature_name, np.nan)

            if pd.isna(value):
                values.append(np.nan)
                validity_mask.append(False)
            else:
                values.append(float(value))
                validity_mask.append(True)

        latitude = float(row["latitude"])
        longitude = float(row["longitude"])

        return FeatureVector(
            values=np.asarray(values, dtype=np.float32),
            validity_mask=np.asarray(validity_mask, dtype=bool),
            coordinates=(latitude, longitude),
            effective_coordinates=(latitude, longitude),
            source="mock_raster_provider",
            metadata=metadata,
        )

    def get_by_index(self, index: int) -> FeatureVector:
        if index < 0 or index >= len(self.df):
            raise IndexError(f"Index out of range: {index}")

        row = self.df.iloc[index]

        metadata = {
            "row_index": int(index),
            "feature_count": len(self.features),
            "valid_feature_count": int(row[self.features].notna().sum()),
            "mapping_version": "1.0.0",
        }

        return self._row_to_feature_vector(row, metadata)

    def get_by_coordinates(
        self,
        latitude: float,
        longitude: float
    ) -> FeatureVector:
        dlat = self.df["latitude"].astype(float) - float(latitude)
        dlon = self.df["longitude"].astype(float) - float(longitude)

        dist2 = dlat * dlat + dlon * dlon
        nearest_index = int(dist2.idxmin())

        row = self.df.iloc[nearest_index]

        metadata = {
            "row_index": nearest_index,
            "requested_coordinates": (
                float(latitude),
                float(longitude)
            ),
            "distance_squared": float(dist2.iloc[nearest_index]),
            "feature_count": len(self.features),
            "valid_feature_count": int(row[self.features].notna().sum()),
            "mapping_version": "1.0.0",
        }

        return self._row_to_feature_vector(row, metadata)