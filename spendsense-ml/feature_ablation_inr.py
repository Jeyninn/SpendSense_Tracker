import pandas as pd

from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

DATA_DIR = Path("data/synthetic/splits")
OUTPUT_DIR = Path("data/synthetic/experiments")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

train = pd.read_csv(DATA_DIR / "train.csv")
validation = pd.read_csv(DATA_DIR / "validation.csv")

normal_train = train[train["is_anomaly"] == 0].copy()

y_validation = validation["is_anomaly"].astype(int)


# --------------------------------------------------
# FEATURE GROUPS
# --------------------------------------------------

BASE_FEATURES = [
    "log_amount",
    "amount_deviation",
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos"
]

EXPERIMENTS = {
    "v2.0.0_baseline": BASE_FEATURES + [
        "category"
    ],

    "past_median": BASE_FEATURES + [
        "customer_past_median",
        "category"
    ],

    "rolling_mean": BASE_FEATURES + [
        "customer_rolling_mean",
        "category"
    ],

    "category_median": BASE_FEATURES + [
        "customer_category_median",
        "category"
    ],

    "personal_and_category_median": BASE_FEATURES + [
        "customer_past_median",
        "customer_category_median",
        "category"
    ]
}


# --------------------------------------------------
# EVALUATION FUNCTION
# --------------------------------------------------

def evaluate_experiment(name, features):

    numeric_features = [
        feature for feature in features
        if feature != "category"
    ]

    categorical_features = ["category"]

    X_train = normal_train[features]
    X_validation = validation[features]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                StandardScaler(),
                numeric_features
            ),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            )
        ]
    )

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

    model.fit(X_train)

    scores = -model.decision_function(X_validation)

    # Select threshold using validation F1.
    best_threshold = None
    best_f1 = -1

    for threshold in sorted(set(scores)):

        predictions = (scores >= threshold).astype(int)

        current_f1 = f1_score(
            y_validation,
            predictions,
            zero_division=0
        )

        if current_f1 > best_f1:
            best_f1 = current_f1
            best_threshold = threshold

    predictions = (
        scores >= best_threshold
    ).astype(int)

    precision = precision_score(
        y_validation,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_validation,
        predictions,
        zero_division=0
    )

    pr_auc = average_precision_score(
        y_validation,
        scores
    )

    roc_auc = roc_auc_score(
        y_validation,
        scores
    )

    return {
        "experiment": name,
        "features": len(features),
        "threshold": best_threshold,
        "precision": precision,
        "recall": recall,
        "f1": best_f1,
        "pr_auc": pr_auc,
        "roc_auc": roc_auc
    }


# --------------------------------------------------
# RUN EXPERIMENTS
# --------------------------------------------------

results = []

for name, features in EXPERIMENTS.items():

    print(f"\nRunning experiment: {name}")

    result = evaluate_experiment(name, features)

    results.append(result)

    print(f"Precision: {result['precision']:.4f}")
    print(f"Recall:    {result['recall']:.4f}")
    print(f"F1:        {result['f1']:.4f}")
    print(f"PR-AUC:    {result['pr_auc']:.4f}")
    print(f"ROC-AUC:   {result['roc_auc']:.4f}")


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="f1",
    ascending=False
)

results_df.to_csv(
    OUTPUT_DIR / "feature_ablation_results.csv",
    index=False
)

print("\n" + "=" * 65)
print("FEATURE ABLATION RESULTS")
print("=" * 65)

print(results_df.to_string(index=False))

print("\nResults saved to:")
print(OUTPUT_DIR / "feature_ablation_results.csv")