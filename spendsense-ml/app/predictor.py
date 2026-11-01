
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from app.schemas import TransactionRequest

# Load the selected INR model
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "spendsense_inr_model.joblib"
)

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
THRESHOLD = model_data["threshold"]
MODEL_VERSION = model_data["model_version"]


def predict_transaction(transaction: TransactionRequest):

    amount = transaction.amount
    reference_amount = transaction.reference_amount

    # Feature engineering (must match training)
    log_amount = np.log1p(amount)
    amount_deviation = amount / reference_amount

    hour_sin = np.sin(2 * np.pi * transaction.hour / 24)
    hour_cos = np.cos(2 * np.pi * transaction.hour / 24)

    weekday_sin = np.sin(
        2 * np.pi * transaction.day_of_week / 7
    )
    weekday_cos = np.cos(
        2 * np.pi * transaction.day_of_week / 7
    )

    input_data = pd.DataFrame([{
        "log_amount": log_amount,
        "amount_deviation": amount_deviation,
        "hour_sin": hour_sin,
        "hour_cos": hour_cos,
        "weekday_sin": weekday_sin,
        "weekday_cos": weekday_cos,
        "category": transaction.category.lower().strip()
    }])

    # Isolation Forest: lower score_samples = more anomalous
    anomaly_score = float(model.score_samples(input_data)[0])

    # Apply the threshold selected on the validation set
    is_anomaly = anomaly_score < THRESHOLD

    # Severity
    if not is_anomaly:
        severity = "normal"
    elif amount_deviation >= 10:
        severity = "high"
    else:
        severity = "medium"

    # Explanation
    if not is_anomaly:
        explanation = "No unusual spending pattern detected."
    else:
        explanation = (
            f"This ₹{amount:.2f} transaction in "
            f"{transaction.category} is approximately "
            f"{amount_deviation:.1f} times its reference amount."
        )

    return {
        "is_anomaly": bool(is_anomaly),
        "anomaly_score": anomaly_score,
        "severity": severity,
        "explanation": explanation,
        "model_version": MODEL_VERSION
    }
