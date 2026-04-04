from __future__ import annotations

import gc
import json
from pathlib import Path
from typing import Any

import joblib

from backend.inference.orgc_wrapper import ORGCWrapper


class ModelRegistry:
    """
    Runtime model loader optimized for low-memory deployment.

    Models are loaded only when needed, used once, then immediately released.
    No persistent cache is kept in memory.
    """

    def __init__(
        self,
        config_path: str = "config/model_registry.json",
    ):
        self.config_path = Path(config_path)

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

    def _artifact_path(self, target: str, artifact: str) -> str:
        return self.registry["models"][target]["artifacts"][artifact]

    def predict(
        self,
        target: str,
        artifact: str,
        X,
    ) -> Any:
        """
        Load one artifact, run prediction, then free memory immediately.
        """
        path = self._artifact_path(target, artifact)

        if path.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)

            return obj

        model = None

        try:
            model = joblib.load(path, mmap_mode="r")

            # ORGC special wrapper
            if target == "lab__ORGC" and artifact == "mu":
                model = ORGCWrapper(model)

            result = model.predict(X)

            if hasattr(model, "_Booster"):
                del model._Booster

            return result

        finally:
            if model is not None:
                del model

            gc.collect()

    def load_json(
        self,
        target: str,
        artifact: str,
    ) -> dict:
        path = self._artifact_path(target, artifact)

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_targets(self):
        return list(self.registry["models"].keys())

    def describe(self, target: str):
        return self.registry["models"][target]