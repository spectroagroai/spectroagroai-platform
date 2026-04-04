from pathlib import Path
import os
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.api.models import PredictRequest, PredictResponse

PROJECT_ROOT = Path(__file__).resolve().parents[2]
os.chdir(PROJECT_ROOT)

app = FastAPI(
    title="SAFI API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://spectroagroai-platform.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def get_runtime():
    from backend.application.runtime_service_v2 import RuntimeServiceV2

    return RuntimeServiceV2()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "safi-runtime",
        "version": "1.0.0",
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    try:
        runtime = get_runtime()

        return runtime.predict(
            latitude=request.latitude,
            longitude=request.longitude,
            mode=request.mode,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))