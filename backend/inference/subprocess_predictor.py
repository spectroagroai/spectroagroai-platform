from __future__ import annotations

import gc
import json
import sys

import joblib
import pandas as pd

from backend.inference.orgc_wrapper import ORGCWrapper


def main():
    payload = json.loads(sys.stdin.read())

    target = payload["target"]
    artifact = payload["artifact"]
    path = payload["path"]
    columns = payload["columns"]
    values = payload["values"]

    X = pd.DataFrame([values], columns=columns)

    model = None

    try:
        model = joblib.load(path, mmap_mode="r")

        if target == "lab__ORGC" and artifact == "mu":
            model = ORGCWrapper(model)

        prediction = model.predict(X)

        if hasattr(model, "_Booster"):
            try:
                del model._Booster
            except Exception:
                pass

        print(
            json.dumps(
                {
                    "prediction": prediction.tolist()
                }
            )
        )

    finally:
        if model is not None:
            del model

        del X
        gc.collect()


if __name__ == "__main__":
    main()