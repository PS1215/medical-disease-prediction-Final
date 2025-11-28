import pickle
import numpy as np

recommendations = {
    "Cold": "Take warm fluids, rest, and OTC cold medicine.",
    "Flu": "Drink plenty of water and take paracetamol for fever.",
    "COVID": "Isolate, drink fluids, monitor oxygen level, consult doctor.",
    "Allergy": "Avoid allergens and take antihistamines.",
    "Migraine": "Rest in dark room, stay hydrated, avoid stress.",
    "Typhoid": "Take antibiotics only when prescribed by a doctor.",
    "Malaria": "Consult doctor immediately and avoid mosquito bites."
}


# Load saved model, label encoder, and feature columns
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

with open("feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)

# Function to take symptoms and predict disease
def predict_disease(symptoms_dict):
    # Convert symptoms dict to ordered feature array
    input_data = [symptoms_dict.get(col, 0) for col in feature_columns]
    input_data = np.array(input_data).reshape(1, -1)
    
    prediction = model.predict(input_data)[0]
    predicted_label = label_encoder.inverse_transform([prediction])[0]
    return predicted_label


# Example usage
if __name__ == "__main__":
    print("Enter symptoms as 1 (yes) or 0 (no)")

    symptoms = {}
    for col in feature_columns:
        val = int(input(f"Do you have '{col}'? (1/0): "))
        symptoms[col] = val

    result = predict_disease(symptoms)
    print("\n🔍 Predicted Disease:", result)
    print("🩺 Recommendation:", recommendations.get(result, "No recommendation available"))


