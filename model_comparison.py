from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score, confusion_matrix

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "dataset_part_2.csv")
features = ["PayloadMass", "Flights", "GridFins", "Reused", "Legs", "Block",
            "ReusedCount", "Orbit", "LaunchSite"]
X = df[features].copy()
y = df["Class"].astype(int)
for col in X.select_dtypes(include="bool").columns:
    X[col] = X[col].astype(int)
numeric = X.select_dtypes(include="number").columns.tolist()
categorical = [col for col in features if col not in numeric]
preprocessing = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median")),
                       ("scaler", StandardScaler())]), numeric),
    ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                       ("encoder", OneHotEncoder(handle_unknown="ignore"))]), categorical),
])
models = {
    "Logistic Regression": LogisticRegression(max_iter=2000),
    "SVM (RBF)": SVC(kernel="rbf"),
    "Decision Tree": DecisionTreeClassifier(max_depth=4, random_state=42),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
}
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
rows = []
for name, estimator in models.items():
    pipeline = Pipeline([("preprocessing", preprocessing), ("classifier", estimator)])
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")
    pipeline.fit(X_train, y_train)
    predicted = pipeline.predict(X_test)
    cm = confusion_matrix(y_test, predicted, labels=[0, 1])
    rows.append({
        "Model": name,
        "Train CV accuracy": round(float(np.mean(cv_scores)), 4),
        "Test accuracy": round(accuracy_score(y_test, predicted), 4),
        "Balanced accuracy": round(balanced_accuracy_score(y_test, predicted), 4),
        "Failure recall": round(recall_score(y_test, predicted, pos_label=0), 4),
        "Failures missed": int(cm[0, 1]),
        "Confusion matrix": cm.tolist(),
    })
results = pd.DataFrame(rows).sort_values("Train CV accuracy", ascending=False)
print("Historical IBM dataset:", len(df), "launches")
print("Training:", len(X_train), "Test:", len(X_test))
print(results.to_string(index=False))
results.to_csv(ROOT / "model_comparison_results.csv", index=False)
