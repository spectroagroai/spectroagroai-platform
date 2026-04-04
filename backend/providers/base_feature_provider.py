from __future__ import annotations

from abc import ABC, abstractmethod

from backend.providers.feature_vector import FeatureVector


class BaseFeatureProvider(ABC):
    @abstractmethod
    def get_by_coordinates(
        self,
        latitude: float,
        longitude: float,
    ) -> FeatureVector:
        """
        Return SAFI FeatureVector for the requested coordinates.
        """
        raise NotImplementedError