import pandas as pd

from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib


DATA_DIR = Path("data/synthetic/splits")

train = pd.read_csv(DATA_DIR / "train.csv")
validation = pd.read_csv(DATA_DIR / "validation.csv")
test = pd.read_csv(DATA_DIR / "test.csv")

BASE_FEATURES = [
    "log_amount",
    "amount_deviation",
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos",
    "category"
]

FEATURES = BASE_FEATURES + ["customer_past_median"]

NUMERIC = [f for f in FEATURES if f != "category"]

normal_train = train[train["is_anomaly"] == 0]

preprocessor = ColumnTransformer([
    ("numeric", StandardScaler(), NUMERIC),
    ("categorical", OneHotEncoder(handle_unknown="ignore"), ["category"])
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", IsolationForest(
        n_estimators=300,
        contamination="auto",
        random_state=42,
        n_jobs=-1
    ))
])

model.fit(normal_train[FEATURES])

# Select threshold using May validation only.
validation_scores = -model.decision_function(validation[FEATURES])
y_val = validation["is_anomaly"].astype(int)

threshold = None
best_f1 = -1

for candidate in sorted(set(validation_scores)):
    predictions = (validation_scores >= candidate).astype(int)
    score = f1_score(y_val, predictions, zero_division=0)

    if score > best_f1:
        best_f1 = score
        threshold = candidate

# Evaluate on June test.
test_scores = -model.decision_function(test[FEATURES])
y_test = test["is_anomaly"].astype(int)
predictions = (test_scores >= threshold).astype(int)

print("\nPAST MEDIAN MODEL - JUNE TEST RESULTS")
print("Locked threshold:", threshold)
print("Precision:", precision_score(y_test, predictions, zero_division=0))
print("Recall:", recall_score(y_test, predictions, zero_division=0))
print("F1:", f1_score(y_test, predictions, zero_division=0))
print("PR-AUC:", average_precision_score(y_test, test_scores))
print("ROC-AUC:", roc_auc_score(y_test, test_scores))
print("\nConfusion matrix:")
print(confusion_matrix(y_test, predictions))

# Save candidate separately.
joblib.dump({
    "model": model,
    "threshold": float(threshold),
    "features": FEATURES,
    "numeric_features": NUMERIC,
    "categorical_features": ["category"],
    "model_version": "2.1.1",
    "currency": "INR"
}, "models/spendsense_inr_model_v211.joblib")

print("\nCandidate saved: models/spendsense_inr_model_v211.joblib")