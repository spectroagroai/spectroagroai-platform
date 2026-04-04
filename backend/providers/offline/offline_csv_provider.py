import numpy as np
from typing import List, Tuple
from .dataset_loader import SAFIDataset
from .spatial_index import SpatialIndex
from .feature_vector import FeatureVector


DISTANCE_THRESHOLD_KM = 50.0  # قابل للتعديل


class OfflineCSVFeatureProvider:

    def __init__(self, csv_path: str, manifest_path: str):
        data = SAFIDataset(csv_path, manifest_path).load()

        self.features = data["features"]
        self.coords_rad = data["coords_rad"]
        self.coords_deg = data["coords_deg"]

        self.index = SpatialIndex(self.coords_rad)

    async def get_features(self, lat: float, lon: float) -> FeatureVector:
        idx, dist_km = self.index.query(lat, lon)

        if dist_km > DISTANCE_THRESHOLD_KM:
            raise ValueError(
                f"OutOfDomainError: nearest point is {dist_km:.2f} km away"
            )

        values = self.features[idx]
        effective_lat, effective_lon = self.coords_deg[idx]

        validity_mask = np.ones_like(values, dtype=bool)

        return FeatureVector(
            values=values,
            query_lat=lat,
            query_lon=lon,
            effective_lat=effective_lat,
            effective_lon=effective_lon,
            distance_km=dist_km,
            source="offline_csv",
            validity_mask=validity_mask
        )

    async def get_features_batch(
        self,
        queries: List[Tuple[float, float]]
    ) -> List[FeatureVector]:

        coords = np.array(queries)
        coords_rad = np.radians(coords)

        dist_rad, idxs = self.index.tree.query(coords_rad, k=1)

        results = []

        for i, (lat, lon) in enumerate(queries):
            idx = idxs[i][0]
            dist_km = dist_rad[i][0] * 6371.0

            if dist_km > DISTANCE_THRESHOLD_KM:
                raise ValueError(
                    f"OutOfDomainError at index {i}: {dist_km:.2f} km"
                )

            values = self.features[idx]
            effective_lat, effective_lon = self.coords_deg[idx]

            fv = FeatureVector(
                values=values,
                query_lat=lat,
                query_lon=lon,
                effective_lat=effective_lat,
                effective_lon=effective_lon,
                distance_km=dist_km,
                source="offline_csv",
                validity_mask=np.ones_like(values, dtype=bool)
            )

            results.append(fv)

        return results