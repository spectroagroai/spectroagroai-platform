from __future__ import annotations

from typing import Any


class ConsistencyValidator:
    """
    SAFI physical consistency checks.

    These warnings do not stop inference.
    They only reduce confidence later.
    """

    @staticmethod
    def validate(
        predictions: dict[str, Any],
    ) -> list[str]:
        warnings = []

        orgc = predictions["lab__ORGC"]["mean"]
        orgm = predictions["lab__ORGM"]["mean"]
        bdf = predictions["lab__BDFIOD"]["mean"]
        totc = predictions["lab__TOTC"]["mean"]

        expected_orgm = orgc * 1.724

        if abs(orgm - expected_orgm) > 0.05:
            warnings.append(
                "ORGM is inconsistent with ORGC × 1.724 conversion."
            )

        if bdf > 1.8 and orgc > 10:
            warnings.append(
                "High bulk density combined with high organic carbon is physically unusual."
            )

        if totc < orgc:
            warnings.append(
                "TOTC is lower than ORGC, which is physically implausible."
            )

        if bdf < 0.7:
            warnings.append(
                "Very low bulk density detected; possible unsupported domain."
            )

        return warnings