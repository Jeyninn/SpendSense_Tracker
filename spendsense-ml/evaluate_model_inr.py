
import joblib
import pandas as pd
import numpy as np

from pathlib import Path
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

TEST_PATH = Path("data/synthetic/splits/test.csv")
MODEL_PATH = Path("models/spendsense_inr_model.joblib")
OUTPUT_DIR = Path("data/synthetic/splits")

# --------------------------------------------------
# 2. LOAD MODEL AND TEST DATA
# --------------------------------------------------

artifact = joblib.load(MODEL_PATH)

model = artifact["model"]
threshold = artifact["threshold"]
features = artifact["features"]

test = pd.read_csv(TEST_PATH)

print("=" * 60)
print("SPENDSENSE AI - FINAL INR MODEL EVALUATION")
print("=" * 60)

print("\nTest dataset shape:", test.shape)
print("Model version:", artifact["model_version"])
print("Currency:", artifact["currency"])
print("Locked validation threshold:", threshold)

# --------------------------------------------------
# 3. PREPARE TEST DATA
# --------------------------------------------------

X_test = test[features].copy()
y_test = test["is_anomaly"].astype(int)

print("\nActual normal transactions:", (y_test == 0).sum())
print("Actual anomalies:", (y_test == 1).sum())

# --------------------------------------------------
# 4. PREDICT ANOMALY SCORES
# --------------------------------------------------

# Lower decision_function = more unusual.
# Negate the score so higher values mean more anomalous.

test_scores = -model.decision_function(X_test)

# Use the threshold selected on validation data.
test_predictions = (
    test_scores >= threshold
).astype(int)

# --------------------------------------------------
# 5. CALCULATE METRICS
# --------------------------------------------------

precision = precision_score(
    y_test,
    test_predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    test_predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    test_predictions,
    zero_division=0
)

pr_auc = average_precision_score(
    y_test,
    test_scores
)

roc_auc = roc_auc_score(
    y_test,
    test_scores
)

# --------------------------------------------------
# 6. DISPLAY RESULTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("FINAL TEST RESULTS - JUNE 2026")
print("=" * 60)

print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")
print(f"PR-AUC:    {pr_auc:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        test_predictions
    )
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        test_predictions,
        target_names=["Normal", "Anomaly"],
        zero_division=0
    )
)

# --------------------------------------------------
# 7. SAVE TEST PREDICTIONS
# --------------------------------------------------

results = test.copy()

results["anomaly_score"] = test_scores
results["predicted_anomaly"] = test_predictions

results.to_csv(
    OUTPUT_DIR / "test_predictions.csv",
    index=False
)

# --------------------------------------------------
# 8. INSPECT FALSE POSITIVES AND FALSE NEGATIVES
# --------------------------------------------------

false_positives = results[
    (results["is_anomaly"] == 0) &
    (results["predicted_anomaly"] == 1)
]

false_negatives = results[
    (results["is_anomaly"] == 1) &
    (results["predicted_anomaly"] == 0)
]

false_positives.to_csv(
    OUTPUT_DIR / "false_positives.csv",
    index=False
)

false_negatives.to_csv(
    OUTPUT_DIR / "false_negatives.csv",
    index=False
)

print("\nFalse positives:", len(false_positives))
print("False negatives:", len(false_negatives))

print("\nSaved:")
print("- test_predictions.csv")
print("- false_positives.csv")
print("- false_negatives.csv")

print("\nEvaluation completed.")
