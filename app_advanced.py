# app_advanced.py
import streamlit as st
import joblib
import numpy as np
import pandas as pd
from recommendation_data import RECOMMENDATIONS

st.set_page_config(page_title="Personalized Medical Recommender", layout="wide")

ARTIFACT_DIR = "model_artifacts"

@st.cache_resource
def load_artifacts():
    stacked = joblib.load(f"{ARTIFACT_DIR}/stacked_model.pkl")
    label_encoder = joblib.load(f"{ARTIFACT_DIR}/label_encoder.pkl")
    severity_le = joblib.load(f"{ARTIFACT_DIR}/severity_label_encoder.pkl")
    severity_model = joblib.load(f"{ARTIFACT_DIR}/severity_model.pkl")
    scaler = joblib.load(f"{ARTIFACT_DIR}/scaler.pkl")
    feature_cols = joblib.load(f"{ARTIFACT_DIR}/feature_columns.pkl")
    knn = joblib.load(f"{ARTIFACT_DIR}/knn_recommender.pkl")
    knn_y_train = joblib.load(f"{ARTIFACT_DIR}/knn_y_train.pkl")
    return {
        "stacked": stacked,
        "le": label_encoder,
        "sev_le": severity_le,
        "sev_model": severity_model,
        "scaler": scaler,
        "cols": feature_cols,
        "knn": knn,
        "knn_y_train": knn_y_train
    }

art = load_artifacts()
stacked = art["stacked"]
le = art["le"]
sev_le = art["sev_le"]
sev_model = art["sev_model"]
scaler = art["scaler"]
feature_cols = art["cols"]
knn = art["knn"]
knn_y_train = art["knn_y_train"]

st.title("🩺 Advanced ML: Disease Prediction + Personalized Recommendations")

st.markdown(
    """
    **Instructions:** select the symptoms you have. For more predictive power, you may provide severity (0-3).
    """
)

# Build UI: for each feature, provide a slider 0-3
symptom_input = {}
cols = feature_cols
st.sidebar.header("Symptom inputs (0 = none, 1-3 increasing severity)")
for c in cols:
    symptom_input[c] = st.sidebar.slider(c.replace('_',' ').capitalize(), min_value=0, max_value=3, value=0)

# Convert input into DataFrame with same column ordering
input_df = pd.DataFrame([symptom_input], columns=cols)

# Feature engineering (same as training)
input_df['symptom_count'] = input_df.sum(axis=1)
respiratory_cols = [c for c in cols if any(s in c.lower() for s in ['cough','breath','chest','sore_throat','runny'])]
if respiratory_cols:
    input_df['respiratory_score'] = input_df[respiratory_cols].sum(axis=1)
if 'fever' in cols and 'cough' in cols:
    input_df['fever_and_cough'] = input_df['fever'] * input_df['cough']

# Predictions
if st.button("Predict disease & recommendations"):
    X_input = input_df.values  # unscaled used for stacked model prediction
    try:
        probs = stacked.predict_proba(X_input)[0]
    except Exception as e:
        st.error("Model predict_proba failed: " + str(e))
        probs = None

    if probs is not None:
        # Build probability table
        prob_df = pd.DataFrame({
            "disease": le.inverse_transform(np.arange(len(probs))),
            "probability": probs
        }).sort_values("probability", ascending=False).reset_index(drop=True)

        st.subheader("Predicted diseases (top candidates)")
        display_df = prob_df.head(8).copy()
        display_df["probability"] = (display_df["probability"] * 100).round(2).astype(str) + "%"
        st.dataframe(display_df)

        # Top prediction
        top_d = prob_df.loc[0, 'disease']
        top_prob = prob_df.loc[0, 'probability']
        st.success(f"Top prediction: **{top_d}** ({top_prob*100:.1f}% confidence)")

        # Severity prediction (use scaled features)
        X_scaled = scaler.transform(input_df.values)
        sev_pred = sev_model.predict(X_scaled)[0]
        sev_label = sev_le.inverse_transform([sev_pred])[0]
        st.info(f"Predicted severity: **{sev_label}**")

        # Recommendation lookup (curated)
        rec = RECOMMENDATIONS.get(top_d, {})
        st.subheader("Human-readable recommendation")
        if rec:
            st.write("**Summary:**", rec.get("summary"))
            st.write("**Home care:**")
            for r in rec.get("home_care", []):
                st.write("- " + r)
            st.write("**Red flags:**")
            for r in rec.get("red_flags", []):
                st.write("- " + r)
            st.write("**Suggested tests:**", ", ".join(rec.get("tests", []) or ["None listed"]))
            st.write("**Advice:**", rec.get("advice", "See physician"))
        else:
            st.write("No curated recommendation available for this disease.")

        # KNN-based similar cases (nearest neighbors)
        neigh_idx = knn.kneighbors(X_scaled, n_neighbors=5, return_distance=False)[0]
        try:
            neighbor_diseases = le.inverse_transform(knn_y_train[neigh_idx])
            st.subheader("Similar past cases (KNN nearest neighbors)")
            for i, nd in enumerate(neighbor_diseases):
                st.write(f"Neighbor {i+1}: Disease = **{nd}**")
        except Exception as e:
            st.write("Could not retrieve neighbor labels:", str(e))
            st.write("Fallback: showing top predicted diseases.")
            for i in range(min(3, len(prob_df))):
                st.write(f"- {prob_df.loc[i,'disease']}: {(prob_df.loc[i,'probability']*100):.1f}%")

        # Probability distribution bar chart
        st.subheader("Probability distribution (top 10)")
        st.bar_chart(prob_df.set_index("disease").head(10).probability)
    else:
        st.error("Prediction failed. See logs.")
