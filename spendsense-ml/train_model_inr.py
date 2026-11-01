
import joblib
import numpy as np
import pandas as pd

from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    precision_recall_curve,
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix
)

# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

DATA_DIR = Path("data/synthetic/splits")
MODEL_DIR = Path("models")

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "spendsense_inr_model.joblib"

NUMERIC_FEATURES = [
    "log_amount",
    "amount_deviation",
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos"
]

CATEGORICAL_FEATURES = [
    "category"
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

RANDOM_STATE = 42


# --------------------------------------------------
# 2. LOAD DATASETS
# --------------------------------------------------

train = pd.read_csv(DATA_DIR / "train.csv")
validation = pd.read_csv(DATA_DIR / "validation.csv")

print("=" * 60)
print("SPENDSENSE AI - INR MODEL TRAINING")
print("=" * 60)

print("\nTraining dataset:", train.shape)
print("Validation dataset:", validation.shape)


# --------------------------------------------------
# 3. PREPARE INPUTS
# --------------------------------------------------

X_train = train[FEATURES].copy()
y_train = train["is_anomaly"].astype(int)

X_validation = validation[FEATURES].copy()
y_validation = validation["is_anomaly"].astype(int)

# Train only on normal transactions.
X_train_normal = X_train[y_train == 0].copy()

print("\nTraining transactions:")
print("Normal transactions:", len(X_train_normal))
print("Excluded injected anomalies:", int(y_train.sum()))


# --------------------------------------------------
# 4. PREPROCESSING PIPELINE
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            StandardScaler(),
            NUMERIC_FEATURES
        ),
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            CATEGORICAL_FEATURES
        )
    ]
)


# --------------------------------------------------
# 5. ISOLATION FOREST
# --------------------------------------------------

isolation_forest = IsolationForest(
    n_estimators=300,
    contamination="auto",
    random_state=RANDOM_STATE,
    n_jobs=-1
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("isolation_forest", isolation_forest)
    ]
)


# --------------------------------------------------
# 6. TRAIN MODEL
# --------------------------------------------------

print("\nTraining Isolation Forest...")

model.fit(X_train_normal)

print("Training completed!")


# --------------------------------------------------
# 7. CALCULATE VALIDATION ANOMALY SCORES
# --------------------------------------------------

# Lower decision_function values indicate more unusual
# transactions. Negating the scores makes higher values
# represent more anomalous transactions.

validation_scores = -model.decision_function(X_validation)

precision_values, recall_values, thresholds = (
    precision_recall_curve(
        y_validation,
        validation_scores
    )
)

# The final precision/recall point has no corresponding
# threshold, so exclude it when calculating F1.

f1_values = (
    2 * precision_values[:-1] * recall_values[:-1]
    / (
        precision_values[:-1] + recall_values[:-1] + 1e-12
    )
)

best_index = int(np.argmax(f1_values))
best_threshold = float(thresholds[best_index])

print("\nValidation threshold selected:")
print(best_threshold)


# --------------------------------------------------
# 8. VALIDATION EVALUATION
# --------------------------------------------------

validation_predictions = (
    validation_scores >= best_threshold
).astype(int)

precision = precision_score(
    y_validation,
    validation_predictions,
    zero_division=0
)

recall = recall_score(
    y_validation,
    validation_predictions,
    zero_division=0
)

f1 = f1_score(
    y_validation,
    validation_predictions,
    zero_division=0
)

pr_auc = average_precision_score(
    y_validation,
    validation_scores
)

roc_auc = roc_auc_score(
    y_validation,
    validation_scores
)

print("\n" + "=" * 60)
print("VALIDATION RESULTS")
print("=" * 60)

print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")
print(f"PR-AUC:    {pr_auc:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")

print("\nConfusion matrix:")
print(
    confusion_matrix(
        y_validation,
        validation_predictions
    )
)


# --------------------------------------------------
# 9. SAVE VALIDATION PREDICTIONS
# --------------------------------------------------

validation_results = validation.copy()

validation_results["anomaly_score"] = validation_scores
validation_results["predicted_anomaly"] = validation_predictions

validation_results.to_csv(
    DATA_DIR / "validation_predictions.csv",
    index=False
)


# --------------------------------------------------
# 10. SAVE MODEL AND THRESHOLD
# --------------------------------------------------

model_artifact = {
    "model": model,
    "threshold": best_threshold,
    "features": FEATURES,
    "numeric_features": NUMERIC_FEATURES,
    "categorical_features": CATEGORICAL_FEATURES,
    "model_version": "2.0.0",
    "currency": "INR"
}

joblib.dump(model_artifact, MODEL_PATH)

print("\n" + "=" * 60)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 60)

print("Model path:", MODEL_PATH)
print("Model version: 2.0.0")
print("Currency: INR")
print("Threshold:", best_threshold)
