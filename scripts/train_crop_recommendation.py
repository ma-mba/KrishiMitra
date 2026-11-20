# train_crop_recommendation.py
"""Training script for Crop Recommendation model.

- Loads dataset from `data/crop_recommendation.csv`.
- Performs basic cleaning, validation, and preprocessing.
- Splits data (80/20) with stratified sampling, fixed random_state=42.
- Trains DecisionTree, RandomForest, GradientBoosting (from scikit-learn).
- Evaluates using accuracy and macroâ€‘F1, prints a concise report.
- Saves the best model, the label encoder, and a simple feature metadata dict
  to `models/crop_recommendation_model.joblib`.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "crop_recommendation.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "crop_recommendation_model.joblib")
METADATA_PATH = os.path.join(MODEL_DIR, "crop_recommendation_metadata.json")

# ---------------------------------------------------------------------------
# 1. Load dataset
# ---------------------------------------------------------------------------
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
print(f"Dataset shape: {df.shape}")
print("First rows:")
print(df.head())

# Expected columns
expected_cols = {"N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"}
missing = expected_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing expected columns: {missing}")

# ---------------------------------------------------------------------------
# 2. Basic validation & cleaning
# ---------------------------------------------------------------------------
# Drop rows with any missing values (there are few in this public dataset)
print("Dropping rows with missing values...")
initial_len = len(df)
df = df.dropna()
print(f"Dropped {initial_len - len(df)} rows (missing values).")



before_dup = len(df)
df = df.drop_duplicates()
before_dup = len(df)
df = df.drop_duplicates()

# Validate ranges (simple sanity checks)
# N, P, K should be nonâ€‘negative and reasonable (0â€‘200). Temperature -10â€‘50Â°C, humidity 0â€‘100%, ph 0â€‘14, rainfall 0â€‘5000 mm.
range_checks = {
    "N": (0, 200),
    "P": (0, 200),
    "K": (0, 200),
    "temperature": (-10, 50),
    "humidity": (0, 100),
    "ph": (0, 14),
    "rainfall": (0, 5000),
}
invalid_rows = []
for col, (lo, hi) in range_checks.items():
    mask = (df[col] < lo) | (df[col] > hi)
    if mask.any():
        invalid = df[mask]
        invalid_rows.append((col, len(invalid)))
        # Clip to the allowed range to keep data usable
        df.loc[mask, col] = np.clip(df.loc[mask, col], lo, hi)
if invalid_rows:
    print("Adjusted outâ€‘ofâ€‘range values:")
    for col, cnt in invalid_rows:
        print(f"  {col}: {cnt} rows")

# ---------------------------------------------------------------------------
# 3. Encode target labels
# ---------------------------------------------------------------------------
le = LabelEncoder()
df["label_enc"] = le.fit_transform(df["label"])
label_mapping = {i: label for i, label in enumerate(le.classes_)}
print("Label mapping (index â†’ crop):")
for i, label in label_mapping.items():
    print(f"  {i}: {label}")

# Features / target
feature_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
X = df[feature_cols].values
y = df["label_enc"].values

# ---------------------------------------------------------------------------
# 4. Trainâ€‘test split (stratified)
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

# ---------------------------------------------------------------------------
# 5. Model training & evaluation helper
# ---------------------------------------------------------------------------
def evaluate_model(model, X_tr, y_tr, X_te, y_te):
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_te)
    acc = accuracy_score(y_te, y_pred)
    macro_f1 = f1_score(y_te, y_pred, average="macro")
    return {
        "model": model,
        "accuracy": acc,
        "macro_f1": macro_f1,
        "report": classification_report(y_te, y_pred, target_names=le.classes_, output_dict=True),
        "confusion": confusion_matrix(y_te, y_pred).tolist(),
    }

# ---------------------------------------------------------------------------
# 6. Train candidate models
# ---------------------------------------------------------------------------
candidates = {
    "DecisionTree": DecisionTreeClassifier(random_state=42),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    "GradientBoosting": GradientBoostingClassifier(random_state=42),
}
results = {}
for name, clf in candidates.items():
    print(f"Training {name}...")
    res = evaluate_model(clf, X_train, y_train, X_test, y_test)
    results[name] = res
    print(f"  Accuracy: {res['accuracy']:.4f}, Macroâ€‘F1: {res['macro_f1']:.4f}")

# ---------------------------------------------------------------------------
# 7. Select best model (by macroâ€‘F1, then accuracy)
# ---------------------------------------------------------------------------
best_name = max(results, key=lambda n: (results[n]["macro_f1"], results[n]["accuracy"]))
best = results[best_name]
print(f"\nBest model: {best_name} (Macroâ€‘F1={best['macro_f1']:.4f}, Acc={best['accuracy']:.4f})")

# ---------------------------------------------------------------------------
# 8. Save model and auxiliary artifacts
# ---------------------------------------------------------------------------
print(f"Saving model to {MODEL_PATH} ...")
joblib.dump({
    "model": best["model"],
    "label_encoder": le,
    "features": feature_cols,
}, MODEL_PATH)

# Save a small metadata JSON for human reference
metadata = {
    "features": feature_cols,
    "label_mapping": label_mapping,
    "best_model": best_name,
    "metrics": {
        "accuracy": best["accuracy"],
        "macro_f1": best["macro_f1"],
    },
    "train_test_split": {
        "train_size": int(len(y_train)),
        "test_size": int(len(y_test)),
        "random_state": 42,
        "stratify": True,
    },
}
with open(METADATA_PATH, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)
print("Training completed and artifacts saved.")


