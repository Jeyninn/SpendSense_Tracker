
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline

# 1. Load training data
train_df = pd.read_csv("data/processed/train.csv")

# 2. Select model features
numerical_features = [
    "log_amount",
    "amount_deviation",
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos"
]

categorical_features = ["category"]

all_features = numerical_features + categorical_features

# 3. Use customers with sufficient personal history
model_df = train_df[
    train_df["has_personal_history"] == 1
].copy()

X_train = model_df[all_features]

print("Training transactions:", len(X_train))

# 4. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            numerical_features
        ),
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)

# 5. Create Isolation Forest
isolation_forest = IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42,
    n_jobs=-1
)

# 6. Create complete pipeline
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("isolation_forest", isolation_forest)
    ]
)

# 7. Train
print("\nTraining Isolation Forest...")

model.fit(X_train)

# 8. Save trained model
joblib.dump(
    model,
    "spendsense_model.joblib"
)

print("\nModel trained successfully!")
print("Model saved as spendsense_model.joblib")

# 9. Display training anomaly distribution
predictions = model.predict(X_train)

normal_count = (predictions == 1).sum()
anomaly_count = (predictions == -1).sum()

print("\n========== TRAINING RESULTS ==========")
print("Normal transactions:", normal_count)
print("Anomalies:", anomaly_count)
print(
    "Anomaly percentage:",
    round(anomaly_count / len(predictions) * 100, 2),
    "%"
)
