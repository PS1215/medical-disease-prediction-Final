import pandas as pd
import random

symptoms = [
    "fever","cough","cold","fatigue","headache","sore_throat","runny_nose",
    "body_pain","chest_pain","nausea","vomiting","diarrhoea",
    "breath_shortness","itchy_skin","rash","joint_pain"
]

diseases = {
    "Common Cold":      ["cough","cold","sore_throat","runny_nose"],
    "Flu":              ["fever","cough","fatigue","headache","body_pain"],
    "COVID":            ["fever","cough","fatigue","breath_shortness","chest_pain"],
    "Migraine":         ["headache","fatigue","joint_pain"],
    "Food Poisoning":   ["nausea","vomiting","diarrhoea","fever"],
    "Dengue":           ["fever","body_pain","joint_pain","headache"],
    "Malaria":          ["fever","body_pain","nausea","headache"],
    "Typhoid":          ["fever","fatigue","headache","nausea"],
    "Pneumonia":        ["fever","cough","chest_pain","breath_shortness"],
    "Allergy":          ["itchy_skin","rash","runny_nose"]
}

rows = []

for _ in range(500):
    disease = random.choice(list(diseases.keys()))
    row = []
    for s in symptoms:
        if s in diseases[disease]:
            row.append(1 if random.random() > 0.1 else 0)  # 90% chance
        else:
            row.append(1 if random.random() < 0.05 else 0)  # 5% noise
    row.append(disease)
    rows.append(row)

df = pd.DataFrame(rows, columns=symptoms + ["disease"])
df.to_csv("symptom_disease_dataset_500.csv", index=False)
