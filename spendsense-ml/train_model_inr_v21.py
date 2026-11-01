import joblib
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


# --------------------------------------------------
# PATHS
# --------------------------------------------------

DATA_DIR = Path("data/synthetic/splits")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

TRAIN_PATH = DATA_DIR / "train.csv"
VALIDATION_PATH = DATA_DIR / "validation.csv"

MODEL_PATH = MODEL_DIR / "spendsense_inr_model_v21.joblib"


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

NUMERIC_FEATURES = [
    "log_amount",
    "amount_deviation",
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos",
    "customer_past_median",
    "customer_rolling_mean",
    "customer_category_median",
    "history_count",
    "category_history_count",
]

CATEGORICAL_FEATURES = [
    "category"
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

train = pd.read_csv(TRAIN_PATH)
validation = pd.read_csv(VALIDATION_PATH)

# Only normal transactions are used for training.
normal_train = train[train["is_anomaly"] == 0].copy()

X_train = normal_train[FEATURES]
X_validation = validation[FEATURES]

y_validation = validation["is_anomaly"].astype(int)


# --------------------------------------------------
# PREPROCESSING
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
# MODEL
# --------------------------------------------------

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            IsolationForest(
                n_estimators=300,
                contamination="auto",
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


# --------------------------------------------------
# TRAIN
# --------------------------------------------------

print("Training INR v2.1.0...")

model.fit(X_train)

print("Training completed.")


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

validation_scores = -model.decision_function(X_validation)

threshold_candidates = sorted(
    set(validation_scores)
)

best_threshold = None
best_f1 = -1

for threshold in threshold_candidates:

    predictions = (
        validation_scores >= threshold
    ).astype(int)

    score = f1_score(
        y_validation,
        predictions,
        zero_division=0
    )

    if score > best_f1:
        best_f1 = score
        best_threshold = threshold


validation_predictions = (
    validation_scores >= best_threshold
).astype(int)

print("\nVALIDATION RESULTS")

print("Threshold:", best_threshold)

print(
    "Precision:",
    precision_score(
        y_validation,
        validation_predictions,
        zero_division=0
    )
)

print(
    "Recall:",
    recall_score(
        y_validation,
        validation_predictions,
        zero_division=0
    )
)

print("F1:", best_f1)

print(
    "PR-AUC:",
    average_precision_score(
        y_validation,
        validation_scores
    )
)

print(
    "ROC-AUC:",
    roc_auc_score(
        y_validation,
        validation_scores
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_validation,
        validation_predictions
    )
)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

artifact = {
    "model": model,
    "threshold": float(best_threshold),
    "features": FEATURES,
    "numeric_features": NUMERIC_FEATURES,
    "categorical_features": CATEGORICAL_FEATURES,
    "model_version": "2.1.0",
    "currency": "INR"
}

joblib.dump(artifact, MODEL_PATH)

print("\nModel saved:", MODEL_PATH)
print("Model version: 2.1.0")