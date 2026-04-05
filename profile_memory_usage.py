from pathlib import Path
import gc
import os

import joblib
import pandas as pd
import psutil

from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent

REFERENCE_CSV = PROJECT_ROOT / "artifacts/reference/safi_v1_universe.csv"

MODELS = {
    "CECPH7_p10": PROJECT_ROOT / "artifacts/models/cecph7/lab__CECPH7_p10.joblib",
    "CECPH7_p50": PROJECT_ROOT / "artifacts/models/cecph7/lab__CECPH7_p50.joblib",
    "CECPH7_p90": PROJECT_ROOT / "artifacts/models/cecph7/lab__CECPH7_p90.joblib",

    "ORGC_mu": PROJECT_ROOT / "artifacts/models/orgc/mu_model_fullfit.joblib",

    "BDFIOD_mu": PROJECT_ROOT / "artifacts/models/bdfiod/mu_bayesridge_pipeline.pkl",
    "BDFIOD_sigma": PROJECT_ROOT / "artifacts/models/bdfiod/sigma_ridge_pipeline.pkl",

    "TOTC_low_q05": PROJECT_ROOT / "artifacts/models/totc/regime_low_q05_log1p_pipeline.pkl",
    "TOTC_low_q50": PROJECT_ROOT / "artifacts/models/totc/regime_low_q50_log1p_pipeline.pkl",
    "TOTC_low_q95": PROJECT_ROOT / "artifacts/models/totc/regime_low_q95_log1p_pipeline.pkl",
    "TOTC_mid_q05": PROJECT_ROOT / "artifacts/models/totc/regime_mid_q05_log1p_pipeline.pkl",
    "TOTC_mid_q50": PROJECT_ROOT / "artifacts/models/totc/regime_mid_q50_log1p_pipeline.pkl",
    "TOTC_mid_q95": PROJECT_ROOT / "artifacts/models/totc/regime_mid_q95_log1p_pipeline.pkl",
    "TOTC_high_q05": PROJECT_ROOT / "artifacts/models/totc/regime_high_q05_log1p_pipeline.pkl",
    "TOTC_high_q50": PROJECT_ROOT / "artifacts/models/totc/regime_high_q50_log1p_pipeline.pkl",
    "TOTC_high_q95": PROJECT_ROOT / "artifacts/models/totc/regime_high_q95_log1p_pipeline.pkl",
}

process = psutil.Process(os.getpid())


def mem_mb():
    return process.memory_info().rss / 1024**2


print("=" * 80)
print("SAFI MEMORY PROFILE")
print("=" * 80)

base = mem_mb()
print(f"Initial memory: {base:.1f} MB")

print("\nLoading universe CSV...")

df = pd.read_csv(REFERENCE_CSV, low_memory=True)

float_cols = df.select_dtypes(include=["float64"]).columns
int_cols = df.select_dtypes(include=["int64"]).columns

df[float_cols] = df[float_cols].astype("float32")
df[int_cols] = df[int_cols].astype("int32")

after_csv = mem_mb()
print(f"After CSV load: {after_csv:.1f} MB")
print(f"CSV memory cost: {after_csv - base:.1f} MB")

loaded = {}

for name, path in MODELS.items():
    before = mem_mb()
    print(f"\nLoading {name} ...")

    loaded[name] = joblib.load(path)

    after = mem_mb()

    print(f"Memory after load: {after:.1f} MB")
    print(f"Approx model cost: {after - before:.1f} MB")

print("\n" + "=" * 80)
print(f"TOTAL MEMORY AFTER ALL MODELS: {mem_mb():.1f} MB")
print("=" * 80)

print("\nNow freeing objects...\n")

loaded.clear()
del df

gc.collect()

print(f"Memory after cleanup: {mem_mb():.1f} MB")