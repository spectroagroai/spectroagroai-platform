from __future__ import annotations

import json
from pathlib import Path

import joblib

from backend.inference.orgc_wrapper import ORGCWrapper


class ModelRegistry:
    """
    Loads SAFI model artifacts lazily and caches them.
    """

    def __init__(
        self,
        config_path: str = "config/model_registry.json",
    ):
        self.config_path = Path(config_path)

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

        self._cache: dict[str, object] = {}

    def get(self, target: str, artifact: str):
        key = f"{target}:{artifact}"

        if key in self._cache:
            return self._cache[key]

        path = self.registry["models"][target]["artifacts"][artifact]

        if path.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)
        else:
            obj = joblib.load(path, mmap_mode="r")

        # Special runtime adaptation for ORGC
        if target == "lab__ORGC" and artifact == "mu":
            obj = ORGCWrapper(obj)

        self._cache[key] = obj
        return obj

    def list_targets(self):
        return list(self.registry["models"].keys())

    def describe(self, target: str):
        return self.registry["models"][target]