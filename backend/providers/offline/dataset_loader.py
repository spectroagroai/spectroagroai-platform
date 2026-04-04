import pandas as pd
import json
import numpy as np
from pathlib import Path


class SAFIDataset:
    def __init__(self, csv_path: str, manifest_path: str):
        self.csv_path = Path(csv_path)
        self.manifest_path = Path(manifest_path)

    def load(self):
        # ==============================
        # 1. Load CSV
        # ==============================
        df = pd.read_csv(self.csv_path)

        print(f"✅ CSV loaded: {df.shape}")

        # ==============================
        # 2. Load Manifest
        # ==============================
        with open(self.manifest_path, "r") as f:
            manifest = json.load(f)

        feature_defs = manifest["features"]

        # ✅ استخراج أسماء الفيتشرز الصحيحة
        feature_cols = [f["feature_id"] for f in feature_defs]

        print(f"✅ Manifest features: {len(feature_cols)}")

        # ==============================
        # 3. Contract Validation (CRITICAL)
        # ==============================
        missing = [f for f in feature_cols if f not in df.columns]

        if missing:
            print("\n❌ Missing features in CSV:")
            for m in missing:
                print(" -", m)

            raise ValueError("Feature mismatch between CSV and manifest")

        print("✅ Feature contract validated")

        # ==============================
        # 4. Extract Feature Matrix
        # ==============================
        features = df[feature_cols].values

        # dtype enforcement
        features = features.astype(np.float32)

        # NaN check
        validity_mask = ~np.isnan(features)

        print("⚠️ NaN detected — will be handled by model pipeline")

        # ==============================
        # 5. Extract Coordinates
        # ==============================
        if "latitude" not in df.columns or "longitude" not in df.columns:
            raise ValueError("CSV must contain latitude and longitude columns")

        coords_deg = df[["latitude", "longitude"]].values

        # Convert to radians for BallTree
        coords_rad = np.radians(coords_deg)

        print("✅ Coordinates extracted")

        # ==============================
        # 6. Return structured data
        # ==============================
        return {
            "features": features,
            "coords_rad": coords_rad,
            "coords_deg": coords_deg,
            "feature_cols": feature_cols
        }