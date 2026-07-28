from fastapi import FastAPI

app = FastAPI(
    title="Delivery Performance Intelligence API",
    description="A web application for managing and predicting delivery performance in logistics, powered by ML models trained on the Olist Brazilian E-Commerce dataset.",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}
