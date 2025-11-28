# recommendation_data.py
# These are general, non-medical, informational recommendations.
# Must be reviewed by a qualified medical professional before real use.

RECOMMENDATIONS = {
    "COVID": {
        "summary": "Viral respiratory illness causing fever, cough, fatigue.",
        "home_care": [
            "Rest and maintain hydration",
            "Use paracetamol for fever if appropriate",
            "Monitor oxygen levels if possible",
            "Self-isolate to prevent spreading"
        ],
        "red_flags": [
            "Difficulty breathing",
            "Chest pain or pressure",
            "Persistent high fever",
            "Confusion or severe drowsiness"
        ],
        "tests": ["RT-PCR test", "Rapid Antigen Test"],
        "advice": "Seek medical help if symptoms are moderate or severe."
    },

    "Flu": {
        "summary": "Influenza virus causing fever, cold, cough, and body pain.",
        "home_care": [
            "Drink warm fluids",
            "Take rest and avoid exertion",
            "Use antipyretics if needed"
        ],
        "red_flags": [
            "Breathing difficulty",
            "Very high fever lasting >3 days"
        ],
        "tests": ["Rapid influenza diagnostic test"],
        "advice": "Consult a doctor if symptoms worsen."
    },

    "Common Cold": {
        "summary": "Mild viral infection affecting nose and throat.",
        "home_care": [
            "Rest and drink warm water",
            "Use steam inhalation",
            "Use mild decongestants if appropriate"
        ],
        "red_flags": [
            "High fever lasting more than 3 days",
            "Shortness of breath"
        ],
        "tests": ["Typically no tests required"],
        "advice": "Generally recovers within a week."
    },

    "Pneumonia": {
        "summary": "Lung infection causing cough, fever, and breathing issues.",
        "home_care": [
            "Get adequate rest",
            "Stay hydrated",
            "Consult a doctor for proper medications"
        ],
        "red_flags": [
            "Severe shortness of breath",
            "Chest pain",
            "Blue lips or fingertips"
        ],
        "tests": ["Chest X-ray", "Blood tests", "Pulse oximetry"],
        "advice": "Requires medical evaluation."
    },

    "Dengue": {
        "summary": "Mosquito-borne viral infection causing fever and body pain.",
        "home_care": [
            "Stay hydrated with ORS, juices, water",
            "Rest properly",
            "Avoid painkillers like ibuprofen (use paracetamol only if allowed)"
        ],
        "red_flags": [
            "Bleeding gums or nose",
            "Severe stomach pain",
            "Persistent vomiting",
            "Drop in platelets symptoms (fatigue, dizziness)"
        ],
        "tests": ["NS1 Antigen test", "Dengue IgM/IgG"],
        "advice": "Seek medical help if symptoms are severe."
    },

    "Malaria": {
        "summary": "Mosquito-borne disease causing fever, chills, and sweating.",
        "home_care": [
            "Hydrate properly",
            "Rest in a cool environment",
            "Consult a doctor for antimalarial treatment"
        ],
        "red_flags": [
            "High fever with chills",
            "Altered consciousness",
            "Persistent vomiting"
        ],
        "tests": ["Rapid Diagnostic Test (RDT)", "Blood smear test"],
        "advice": "Treatment should begin after confirmation."
    },

    "Typhoid": {
        "summary": "Bacterial infection causing prolonged fever and abdominal issues.",
        "home_care": [
            "Drink clean water and fluids",
            "Soft, easily digestible food",
            "Doctor consultation for antibiotics"
        ],
        "red_flags": [
            "Severe abdominal pain",
            "Persistent high fever",
            "Diarrhea with dehydration"
        ],
        "tests": ["Blood culture", "Widal test"],
        "advice": "Antibiotics should only be taken after medical consultation."
    },

    "Food Poisoning": {
        "summary": "Illness caused by contaminated food.",
        "home_care": [
            "Oral rehydration salts (ORS)",
            "Avoid solid food until vomiting stops",
            "Eat small, light meals later"
        ],
        "red_flags": [
            "Blood in stool",
            "Continuous vomiting",
            "Signs of dehydration (dry mouth, dizziness)"
        ],
        "tests": ["Stool test (if severe)", "Hydration assessment"],
        "advice": "Seek medical care if symptoms persist."
    },

    "Allergy": {
        "summary": "Reaction to allergens causing sneezing, rash, or itching.",
        "home_care": [
            "Avoid known triggers",
            "Use antihistamines if appropriate",
            "Stay in clean, dust-free areas"
        ],
        "red_flags": [
            "Swelling of face or throat",
            "Breathing difficulty",
            "Severe rashes"
        ],
        "tests": ["Allergy test (IgE)", "Skin prick test"],
        "advice": "Seek immediate care for severe reactions."
    },

    "Migraine": {
        "summary": "Neurological condition causing severe headaches and sensitivity.",
        "home_care": [
            "Rest in a dark, quiet room",
            "Hydrate well",
            "Use prescribed migraine medication if available"
        ],
        "red_flags": [
            "Sudden severe headache",
            "Weakness, numbness, or difficulty speaking",
            "Headache with fever or neck stiffness"
        ],
        "tests": ["Usually clinical diagnosis", "Neurological evaluation if needed"],
        "advice": "Consult a doctor if headaches are frequent or disabling."
    }
}


