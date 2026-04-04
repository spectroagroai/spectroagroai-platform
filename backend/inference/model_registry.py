from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class ModelRegistry:
    """
    Memory-safe model registry.

    Every prediction runs in a separate subprocess so that model memory
    is fully released when the subprocess exits.
    """

    def __init__(
        self,
        config_path: str = "config/model_registry.json",
    ):
        self.config_path = Path(config_path)

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

        self.python_exec = sys.executable

    def _artifact_path(self, target: str, artifact: str) -> str:
        return self.registry["models"][target]["artifacts"][artifact]

    def predict(
        self,
        target: str,
        artifact: str,
        X,
    ) -> Any:
        path = self._artifact_path(target, artifact)

        if path.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        payload = {
            "target": target,
            "artifact": artifact,
            "path": path,
            "columns": list(X.columns),
            "values": X.iloc[0].tolist(),
        }

        result = subprocess.run(
            [
                self.python_exec,
                "-m",
                "backend.inference.subprocess_predictor",
            ],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Subprocess prediction failed:\n"
                f"{result.stderr}\n"
                f"{result.stdout}"
            )

        return json.loads(result.stdout)["prediction"]

    def list_targets(self):
        return list(self.registry["models"].keys())

    def describe(self, target: str):
        return self.registry["models"][target]