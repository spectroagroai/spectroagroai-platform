from __future__ import annotations

import pandas as pd


class ORGCWrapper:
    """
    ORGC was trained with an accidental leading `point_id` column.

    SAFI runtime keeps the canonical 157-feature manifest and injects
    a dummy point_id only for this model.
    """

    def __init__(self, model):
        self.model = model

    def predict(self, X: pd.DataFrame):
        if "point_id" in X.columns:
            raise ValueError(
                "SAFI canonical feature contract must not contain point_id"
            )

        X2 = X.copy()
        X2.insert(0, "point_id", 0)

        return self.model.predict(X2)