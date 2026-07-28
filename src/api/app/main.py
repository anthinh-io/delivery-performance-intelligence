from fastapi import FastAPI

from app.model import predict as run_prediction
from app.schemas import PredictRequest, PredictResponse

app = FastAPI(
    title="Delivery Performance Intelligence API",
    description="A web application for managing and predicting delivery performance in logistics, powered by ML models trained on the Olist Brazilian E-Commerce dataset.",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    return run_prediction(request)
