# backend/providers/offline/offline_csv_feature_provider.py

from __future__ import annotations

from pathlib import Path

import pandas as pd

from backend.inference.inference_engine import InferenceEngine
from backend.providers.feature_vector import FeatureVector
from backend.providers.base_feature_provider import BaseFeatureProvider



ROOT = Path(__file__).resolve().parents[3]
CSV_PATH = ROOT / "artifacts" / "reference" / "safi_v1_universe.csv"


class OfflineCSVFeatureProvider(BaseFeatureProvider):
    """
    Offline SAFI feature provider using safi_v1_universe.csv.

    Current behavior:
    - can retrieve by row index
    - can retrieve nearest point by latitude/longitude
    - returns canonical FeatureVector
    """

    def __init__(self):
        self.engine = InferenceEngine()
        self.features = self.engine.features

        self.df = pd.read_csv(CSV_PATH)

        required_columns = {"latitude", "longitude"}

        missing = required_columns - set(self.df.columns)

        if missing:
            raise ValueError(
                f"safi_v1_universe.csv missing required coordinate columns: {missing}"
            )

    def _build_feature_vector(
        self,
        row: pd.Series,
        coordinates: tuple[float, float],
        effective_coordinates: tuple[float, float],
        metadata: dict,
    ) -> FeatureVector:
        values = {}
        validity_mask = {}

        for feature in self.features:
            value = row.get(feature)

            if pd.notna(value):
                values[feature] = float(value)
                validity_mask[feature] = True
            else:
                values[feature] = float("nan")
                validity_mask[feature] = False

        return FeatureVector(
            values=values,
            validity_mask=validity_mask,
            coordinates=coordinates,
            effective_coordinates=effective_coordinates,
            source="offline_csv",
            metadata=metadata,
        )

    def get_by_index(self, index: int) -> FeatureVector:
        if index < 0 or index >= len(self.df):
            raise IndexError(
                f"Index {index} outside valid range 0..{len(self.df)-1}"
            )

        row = self.df.iloc[index]

        lat = float(row["latitude"])
        lon = float(row["longitude"])

        return self._build_feature_vector(
            row=row,
            coordinates=(lat, lon),
            effective_coordinates=(lat, lon),
            metadata={
                "row_index": int(index),
            },
        )

    def get_by_coordinates(
        self,
        latitude: float,
        longitude: float,
    ) -> FeatureVector:
        dist2 = (
            (self.df["latitude"] - latitude) ** 2
            + (self.df["longitude"] - longitude) ** 2
        )

        nearest_index = int(dist2.idxmin())

        row = self.df.iloc[nearest_index]

        nearest_lat = float(row["latitude"])
        nearest_lon = float(row["longitude"])

        return self._build_feature_vector(
            row=row,
            coordinates=(latitude, longitude),
            effective_coordinates=(nearest_lat, nearest_lon),
            metadata={
                "row_index": nearest_index,
                "requested_coordinates": (
                    float(latitude),
                    float(longitude),
                ),
                "distance_squared": float(dist2.iloc[nearest_index]),
            },
        )