
from fastapi import FastAPI
from app.schemas import TransactionRequest, AnomalyResponse
from app.predictor import predict_transaction

app = FastAPI(
    title="SpendSense AI",
    description="Personalized spending anomaly detection service",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SpendSense AI"
    }


@app.post(
    "/predict",
    response_model=AnomalyResponse
)
def predict(transaction: TransactionRequest):

    # Cold-start fallback
    if not transaction.has_personal_history:
        return {
            "is_anomaly": False,
            "anomaly_score": 0.0,
            "severity": "insufficient_history",
            "explanation": (
                "Not enough personal transaction history "
                "to assess unusual spending reliably."
            ),
            "model_version": "1.0.0"
        }

    return predict_transaction(transaction)
