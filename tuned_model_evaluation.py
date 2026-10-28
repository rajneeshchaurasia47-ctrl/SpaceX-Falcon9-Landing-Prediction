"""Reproducible tuned-model evidence for the SpaceX IBM historical 90-row data.
Training-only GridSearchCV; 23-row untouched holdout. Educational sample.
Run: python tuned_model_evaluation.py
"""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (accuracy_score, balanced_accuracy_score,
                             recall_score, confusion_matrix)

ROOT = Path(__file__).resolve().parent
data = pd.read_csv(ROOT / "dataset_part_2.csv")
cols = ["PayloadMass", "Flights", "GridFins", "Reused", "Legs", "Block",
        "ReusedCount", "Orbit", "LaunchSite"]
X = data[cols].copy()
for name in ["GridFins", "Reused", "Legs"]:
    X[name] = X[name].astype(int)
y = data["Class"].astype(int)
numerical = cols[:7]
categorical = cols[7:]
prep = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ]), numerical),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("enc", OneHotEncoder(handle_unknown="ignore"))
    ]), categorical)
])
Xtrain, Xtest, ytrain, ytest = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
models = {
    "Logistic Regression": (LogisticRegression(max_iter=2000), {"clf__C": [0.1, 1, 10]}),
    "SVM": (SVC(), {"clf__C": [0.1, 1, 10], "clf__kernel": ["linear", "rbf"]}),
    "Decision Tree": (DecisionTreeClassifier(random_state=42),
                      {"clf__max_depth": [2, 3, 4, 5], "clf__min_samples_leaf": [1, 3, 5]}),
    "KNN": (KNeighborsClassifier(), {"clf__n_neighbors": [3, 5, 7, 9]})
}
rows = []
for name, (classifier, search_space) in models.items():
    estimator = Pipeline([("prep", prep), ("clf", classifier)])
    grid = GridSearchCV(estimator, search_space, cv=folds,
                        scoring="balanced_accuracy", n_jobs=-1, refit=True)
    grid.fit(Xtrain, ytrain)
    pred = grid.predict(Xtest)
    cm = confusion_matrix(ytest, pred, labels=[0, 1])
    rows.append({
        "model": name,
        "cv_balanced_accuracy": round(grid.best_score_, 4),
        "test_accuracy": round(accuracy_score(ytest, pred), 4),
        "test_balanced_accuracy": round(balanced_accuracy_score(ytest, pred), 4),
        "failure_recall": round(recall_score(ytest, pred, pos_label=0), 4),
        "failure_missed": int(cm[0, 1]),
        "confusion_matrix": cm.tolist(),
        "best_params": grid.best_params_
    })
results = pd.DataFrame(rows)
print(f"Data={len(data)} | Train={len(Xtrain)} | Test={len(Xtest)}")
print(results.to_string(index=False))
results.to_csv(ROOT / "tuned_model_results.csv", index=False)
