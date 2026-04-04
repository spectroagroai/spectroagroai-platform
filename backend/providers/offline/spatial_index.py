from sklearn.neighbors import BallTree
import numpy as np


EARTH_RADIUS_KM = 6371.0


class SpatialIndex:
    def __init__(self, coords_rad: np.ndarray):
        self.tree = BallTree(coords_rad, metric="haversine")

    def query(self, lat: float, lon: float):
        query_rad = np.radians([[lat, lon]])

        dist_rad, idx = self.tree.query(query_rad, k=1)

        dist_km = dist_rad[0][0] * EARTH_RADIUS_KM
        index = idx[0][0]

        return index, dist_km