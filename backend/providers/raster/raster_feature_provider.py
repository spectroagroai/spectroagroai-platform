from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from backend.providers.base_feature_provider import BaseFeatureProvider
from backend.providers.feature_vector import FeatureVector


class RasterFeatureProvider(BaseFeatureProvider):
    """
    Future production raster-backed SAFI feature provider.

    Current phase:
    - loads raster_feature_mapping.json
    - preserves exact 157-feature manifest order
    - attempts to load raster stacks if they exist
    - returns NaN for unavailable stacks
    """

    def __init__(
        self,
        mapping_path: str = "config/raster_feature_mapping.json",
        grid_path: str = "config/raster_grid.json",
        raster_root: str = "data/rasters/stacks",
    ) -> None:
        self.mapping_path = Path(mapping_path)
        self.grid_path = Path(grid_path)
        self.raster_root = Path(raster_root)

        with open(self.mapping_path, "r", encoding="utf-8") as f:
            raw_mapping = json.load(f)

        # raster_feature_mapping.json may be either:
        # 1) list[dict]
        # 2) {"features": list[dict]}
        if isinstance(raw_mapping, dict):
            self.mapping: List[Dict[str, Any]] = raw_mapping.get("features", [])
        else:
            self.mapping = raw_mapping

        self.feature_names = [entry["feature_name"] for entry in self.mapping]

        if self.grid_path.exists():
            with open(self.grid_path, "r", encoding="utf-8") as f:
                self.grid_config = json.load(f)
        else:
            self.grid_config = {}

        self._stack_cache: Dict[str, Any] = {}

    def get_by_coordinates(
        self,
        latitude: float,
        longitude: float,
    ) -> FeatureVector:
        """
        Main entry point for raster-backed feature extraction.
        """

        effective_lat, effective_lon = self._snap_to_grid(latitude, longitude)

        values = []
        validity_mask = []

        for feature in self.mapping:
            stack_name = feature["stack_name"]
            band_index = feature["band_index"]

            stack = self._load_stack(stack_name)

            if stack is None:
                values.append(np.nan)
                validity_mask.append(False)
                continue

            raw_value = self._sample_band(
                stack=stack,
                band_index=band_index,
                latitude=effective_lat,
                longitude=effective_lon,
            )

            value = self._apply_scale_offset(
                value=raw_value,
                scale_factor=feature.get("scale_factor"),
                add_offset=feature.get("add_offset"),
            )

            values.append(value)
            validity_mask.append(not np.isnan(value))

        values = np.asarray(values, dtype=np.float32)
        validity_mask = np.asarray(validity_mask, dtype=bool)

        loaded_stacks = sorted(
            {
                feature["stack_name"]
                for feature in self.mapping
                if self._load_stack(feature["stack_name"]) is not None
            }
        )

        metadata = {
            "provider": "raster_feature_provider",
            "mapping_version": str(self.mapping_path),
            "grid_source": str(self.grid_path),
            "raster_root": str(self.raster_root),
            "feature_count": len(values),
            "valid_feature_count": int(validity_mask.sum()),
            "loaded_stacks": loaded_stacks,
        }

        return FeatureVector(
            values=values,
            validity_mask=validity_mask,
            coordinates=(latitude, longitude),
            effective_coordinates=(effective_lat, effective_lon),
            source="raster",
            metadata=metadata,
        )

    def _snap_to_grid(
        self,
        latitude: float,
        longitude: float,
    ) -> tuple[float, float]:
        """
        Temporary placeholder snapping based on raster_grid.json.

        Later this must use actual raster metadata.
        """

        resolution = self.grid_config.get("resolution", 0.0011139)

        snapped_lat = round(latitude / resolution) * resolution
        snapped_lon = round(longitude / resolution) * resolution

        return snapped_lat, snapped_lon

    def _load_stack(self, stack_name: str) -> Any:
        """
        Load and cache raster stack.

        Expected future location:
        data/rasters/stacks/<stack_name>.tif
        """

        if stack_name in self._stack_cache:
            return self._stack_cache[stack_name]

        stack_path = self.raster_root / f"{stack_name}.tif"

        if not stack_path.exists():
            self._stack_cache[stack_name] = None
            return None

        try:
            import rasterio

            dataset = rasterio.open(stack_path)
            self._stack_cache[stack_name] = dataset
            return dataset

        except Exception as exc:
            print(f"⚠️ Failed to load stack '{stack_name}': {exc}")
            self._stack_cache[stack_name] = None
            return None

    def _sample_band(
        self,
        stack: Any,
        band_index: int,
        latitude: float,
        longitude: float,
    ) -> float:
        """
        Sample one raster band at the requested coordinate.
        Converts nodata values into NaN.
        """

        try:
            row, col = stack.index(longitude, latitude)

            band = stack.read(band_index)
            value = band[row, col]

            nodata = stack.nodata

            if nodata is not None and value == nodata:
                return np.nan

            return float(value)

        except Exception:
            return np.nan

    def _apply_scale_offset(
        self,
        value: float,
        scale_factor: float | None,
        add_offset: float | None,
    ) -> float:
        """
        Apply scale_factor and add_offset defined in raster_feature_mapping.json.
        """

        if np.isnan(value):
            return value

        if scale_factor is not None:
            value = value * scale_factor

        if add_offset is not None:
            value = value + add_offset

        return value