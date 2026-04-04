from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DOMAIN_RULES_PATH = ROOT / "config" / "domain_rules.json"


class DomainValidator:
    """
    SAFI v1 domain validator.

    Validates that all feature values fall inside the supported
    training-domain limits defined in config/domain_rules.json.
    """

    _rules: dict[str, dict[str, float]] | None = None

    @classmethod
    def _load_rules(cls) -> dict[str, dict[str, float]]:
        if cls._rules is not None:
            return cls._rules

        if not DOMAIN_RULES_PATH.exists():
            cls._rules = {}
            return cls._rules

        with open(DOMAIN_RULES_PATH, "r", encoding="utf-8") as f:
            cls._rules = json.load(f)

        return cls._rules

    @classmethod
    def validate(
        cls,
        feature_values: dict[str, Any],
    ) -> list[str]:
        rules = cls._load_rules()

        errors: list[str] = []

        for feature_name, value in feature_values.items():
            if feature_name not in rules:
                continue

            if value is None:
                continue

            try:
                numeric_value = float(value)
            except Exception:
                errors.append(
                    f"{feature_name}: value '{value}' is not numeric"
                )
                continue

            rule = rules[feature_name]

            min_value = rule.get("min")
            max_value = rule.get("max")

            if min_value is not None and numeric_value < min_value:
                errors.append(
                    f"{feature_name}: {numeric_value} is below minimum {min_value}"
                )

            if max_value is not None and numeric_value > max_value:
                errors.append(
                    f"{feature_name}: {numeric_value} exceeds maximum {max_value}"
                )

        return errors
