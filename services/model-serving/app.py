from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Model Serving Service")


class PredictRequest(BaseModel):
    instances: List[float]


class PredictResponse(BaseModel):
    predictions: List[float]


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest) -> PredictResponse:
    outputs = [x * 2 for x in request.instances]
    return PredictResponse(predictions=outputs)


@app.get("/health")
async def health():
    return {"status": "ok"}
