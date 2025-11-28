# train_advanced.py
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb

DATA_PATH = "symptom_disease_dataset_500.csv"
OUT_DIR = "model_artifacts"

os.makedirs(OUT_DIR, exist_ok=True)

# ---------- 1) Load dataset ----------
df = pd.read_csv(DATA_PATH)
print("Loaded dataset shape:", df.shape)

# Detect label column (fall back to last column)
possible_labels = [c for c in df.columns if 'disease' in c.lower() or c.lower() in ('label','target','diagnosis')]
label_col = possible_labels[0] if possible_labels else df.columns[-1]
print("Using label column:", label_col)

# Features and labels
X = df.drop(columns=[label_col]).copy()
y = df[label_col].astype(str).copy()

# ---------- 2) Basic preprocessing ----------
for col in X.columns:
    if X[col].dtype == object:
        vals = set([str(v).lower() for v in X[col].dropna().unique()])
        if vals <= {'yes','no','y','n'}:
            X[col] = X[col].map(lambda v: 1 if str(v).lower().startswith('y') else 0)
        else:
            if X[col].nunique() <= 6:
                dummies = pd.get_dummies(X[col], prefix=col, drop_first=True)
                X = pd.concat([X.drop(columns=[col]), dummies], axis=1)
            else:
                X = X.drop(columns=[col])

# ---------- 3) Feature engineering ----------
X['symptom_count'] = X.sum(axis=1)

respiratory_cols = [c for c in X.columns if any(s in c.lower() for s in ['cough','breath','chest','sore_throat','runny'])]
if respiratory_cols:
    X['respiratory_score'] = X[respiratory_cols].sum(axis=1)

if 'fever' in X.columns and 'cough' in X.columns:
    X['fever_and_cough'] = X['fever'] * X['cough']

print("Feature engineering done. Final feature count:", X.shape[1])

# ---------- 4) Severity labels (synthetic if absent) ----------
if 'severity' in df.columns:
    severity_labels = df['severity'].astype(str)
    has_real_severity = True
else:
    def to_severity(n):
        if n <= 2:
            return 'Mild'
        elif n <= 4:
            return 'Moderate'
        else:
            return 'Severe'
    severity_labels = X['symptom_count'].apply(to_severity)
    has_real_severity = False
print("Severity label creation done. Using real severity:", has_real_severity)

# ---------- 5) Encode labels ----------
le = LabelEncoder()
y_enc = le.fit_transform(y)
print("Disease classes:", le.classes_)

le_sev = LabelEncoder()
sev_enc = le_sev.fit_transform(severity_labels)

# Save encoders
joblib.dump(le, os.path.join(OUT_DIR, "label_encoder.pkl"))
joblib.dump(le_sev, os.path.join(OUT_DIR, "severity_label_encoder.pkl"))

# ---------- 6) Train-test split ----------
X_train, X_test, y_train, y_test, sev_train, sev_test = train_test_split(
    X, y_enc, sev_enc, test_size=0.2, random_state=42, stratify=y_enc
)
print("Train/test split:", X_train.shape, X_test.shape)

# Save y_train for KNN neighbor label lookup (IMPORTANT)
joblib.dump(y_train, os.path.join(OUT_DIR, "knn_y_train.pkl"))

# ---------- 7) Preprocessing: scaler for some models ----------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
joblib.dump(scaler, os.path.join(OUT_DIR, "scaler.pkl"))

# ---------- 8) Base models ----------
rf = RandomForestClassifier(n_estimators=300, random_state=42)
xg = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
svc = SVC(probability=True, kernel='rbf', random_state=42)
mlp = MLPClassifier(hidden_layer_sizes=(64,32), max_iter=500, random_state=42)

# Fit base models (some on unscaled, some on scaled)
rf.fit(X_train, y_train)
xg.fit(X_train, y_train)
svc.fit(X_train_scaled, y_train)
mlp.fit(X_train_scaled, y_train)

# ---------- 9) Stacking ensemble ----------
estimators = [
    ('rf', rf),
    ('xg', xg),
    ('svc', svc),
    ('mlp', mlp)
]
meta_clf = LogisticRegression(max_iter=1000)
stack = StackingClassifier(estimators=estimators, final_estimator=meta_clf, cv=5, passthrough=False, n_jobs=-1)
stack.fit(X_train, y_train)
joblib.dump(stack, os.path.join(OUT_DIR, "stacked_model.pkl"))
print("Saved stacked model.")

# ---------- 10) Evaluate stacked model ----------
y_pred = stack.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Stacked model accuracy: {acc:.4f}")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Save base models (optional)
joblib.dump(rf, os.path.join(OUT_DIR, "rf_model.pkl"))
joblib.dump(xg, os.path.join(OUT_DIR, "xg_model.pkl"))
joblib.dump(svc, os.path.join(OUT_DIR, "svc_model.pkl"))
joblib.dump(mlp, os.path.join(OUT_DIR, "mlp_model.pkl"))

# ---------- 11) Train severity classifier ----------
sev_clf = RandomForestClassifier(n_estimators=200, random_state=42)
sev_clf.fit(X_train, sev_train)
joblib.dump(sev_clf, os.path.join(OUT_DIR, "severity_model.pkl"))
sev_pred = sev_clf.predict(X_test)
print("Severity classifier accuracy:", accuracy_score(sev_test, sev_pred))
print(classification_report(sev_test, sev_pred, target_names=le_sev.classes_))

# ---------- 12) Build and save KNN recommender ----------
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
# fit KNN on scaled features and use y_train (encoded labels)
knn.fit(X_train_scaled, y_train)
joblib.dump(knn, os.path.join(OUT_DIR, "knn_recommender.pkl"))

# Save feature column order
joblib.dump(list(X.columns), os.path.join(OUT_DIR, "feature_columns.pkl"))

print("All artifacts saved inside", OUT_DIR)
