from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from backend.providers.base_feature_provider import BaseFeatureProvider
from backend.providers.feature_vector import FeatureVector
from backend.providers.offline.spatial_index import SpatialIndex


ROOT = Path(__file__).resolve().parents[3]

CSV_PATH = ROOT / "artifacts" / "reference" / "safi_v1_universe.csv"
MANIFEST_PATH = ROOT / "config" / "safi_covariate_manifest_v5.json"

DISTANCE_THRESHOLD_KM = 5000.0


class OfflineCSVFeatureProvider(BaseFeatureProvider):
    """
    Memory-optimized offline provider.

    Keeps only:
    - float32 feature matrix
    - coordinate arrays
    - BallTree index
    """

    def __init__(self):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.features = [
            item["feature_id"]
            for item in manifest["features"]
        ]

        required_columns = (
            ["latitude", "longitude"] + self.features
        )

        df = pd.read_csv(
            CSV_PATH,
            usecols=lambda c: c in required_columns,
            low_memory=True,
        )

        float_cols = [
            c for c in df.columns
            if c not in ("latitude", "longitude")
        ]

        df[float_cols] = df[float_cols].astype(np.float32)
        df["latitude"] = df["latitude"].astype(np.float32)
        df["longitude"] = df["longitude"].astype(np.float32)

        self.feature_matrix = df[self.features].to_numpy(dtype=np.float32)

        self.coords_deg = df[
            ["latitude", "longitude"]
        ].to_numpy(dtype=np.float32)

        self.coords_rad = np.radians(self.coords_deg)

        self.index = SpatialIndex(self.coords_rad)

        # Free dataframe memory immediately
        del df

    def _build_feature_vector(
        self,
        row_index: int,
        query_lat: float,
        query_lon: float,
        dist_km: float,
    ) -> FeatureVector:
        values_array = self.feature_matrix[row_index]

        values = {}
        validity_mask = {}

        for idx, feature_name in enumerate(self.features):
            value = values_array[idx]

            if np.isnan(value):
                values[feature_name] = float("nan")
                validity_mask[feature_name] = False
            else:
                values[feature_name] = float(value)
                validity_mask[feature_name] = True

        effective_lat = float(self.coords_deg[row_index][0])
        effective_lon = float(self.coords_deg[row_index][1])

        return FeatureVector(
            values=values,
            validity_mask=validity_mask,
            coordinates=(float(query_lat), float(query_lon)),
            effective_coordinates=(effective_lat, effective_lon),
            source="offline_csv",
            metadata={
                "row_index": int(row_index),
                "distance_km": float(dist_km),
            },
        )

    def get_by_index(self, index: int) -> FeatureVector:
        if index < 0 or index >= len(self.feature_matrix):
            raise IndexError(
                f"Index {index} خارج المجال"
            )

        lat = float(self.coords_deg[index][0])
        lon = float(self.coords_deg[index][1])

        return self._build_feature_vector(
            row_index=index,
            query_lat=lat,
            query_lon=lon,
            dist_km=0.0,
        )

    def get_by_coordinates(
        self,
        latitude: float,
        longitude: float,
    ) -> FeatureVector:
        row_index, dist_km = self.index.query(
            latitude,
            longitude,
        )

        if dist_km > DISTANCE_THRESHOLD_KM:
            raise ValueError(
                f"Nearest SAFI reference point is too far: "
                f"{dist_km:.2f} km"
            )

        return self._build_feature_vector(
            row_index=row_index,
            query_lat=latitude,
            query_lon=longitude,
            dist_km=dist_km,
        )