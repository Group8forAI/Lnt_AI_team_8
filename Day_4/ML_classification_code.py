import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel dataset
file_path = 'Indian_Major_Carps_Dataset.xlsx'
df = pd.read_excel(file_path, sheet_name='Main_Dataset')

# Define input features and target outputs
features = [
    'Tank_ID', 'Carp_Species', 'Temperature_C', 'Dissolved_Oxygen_mgL',
    'pH', 'Ammonia_mgL', 'Nitrate_mgL', 'Turbidity_NTU',
    'Alkalinity_mgL', 'Hardness_mgL', 'Soil_Moisture'
]

targets = [
    'Tank_Leakage', 'Temperature_Status', 'Water_Quality_Index',
    'DO_Status', 'Growth_Condition'
]

# Encode categorical input features
carp_encoder = LabelEncoder()
df['Carp_Species'] = carp_encoder.fit_transform(df['Carp_Species'])

# Encode categorical output labels
label_encoders = {}
for col in targets:
    if df[col].dtype == 'object':
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

# Split dataset into features and labels
X = df[features]
y = df[targets]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest with MultiOutputClassifier
model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
model.fit(X_train, y_train)

# Evaluate each output
y_pred = model.predict(X_test)
for i, target in enumerate(targets):
    print(f"\n🎯 Classification Report for: {target}")
    print(classification_report(y_test.iloc[:, i], y_pred[:, i]))

# Plot feature importance for each target output
for i, target in enumerate(targets):
    importances = model.estimators_[i].feature_importances_
    plt.figure(figsize=(10, 5))
    sns.barplot(x=importances, y=X.columns, palette='coolwarm')
    plt.title(f'Feature Importance for: {target}')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.show()

# Prediction Interface
def predict_from_input():
    print("\n🔍 Enter Input Feature Values:")
    user_input = {}
    user_input['Tank_ID'] = int(input("Tank ID (e.g., 1): "))

    species_list = list(carp_encoder.classes_)
    print("Available Carp Species:", species_list)
    species_input = input("Carp Species (exact from above): ")
    user_input['Carp_Species'] = carp_encoder.transform([species_input])[0]

    user_input['Temperature_C'] = float(input("Temperature (°C): "))
    user_input['Dissolved_Oxygen_mgL'] = float(input("Dissolved Oxygen (mg/L): "))
    user_input['pH'] = float(input("pH: "))
    user_input['Ammonia_mgL'] = float(input("Ammonia (mg/L): "))
    user_input['Nitrate_mgL'] = float(input("Nitrate (mg/L): "))
    user_input['Turbidity_NTU'] = float(input("Turbidity (NTU): "))
    user_input['Alkalinity_mgL'] = float(input("Alkalinity (mg/L): "))
    user_input['Hardness_mgL'] = float(input("Hardness (mg/L): "))
    user_input['Soil_Moisture'] = float(input("Soil Moisture: "))

    # Prepare input and predict
    input_df = pd.DataFrame([user_input])
    prediction = model.predict(input_df)[0]

    print("\n📊 Predicted Output Labels:")
    for label, value in zip(targets, prediction):
        if label in label_encoders:
            decoded = label_encoders[label].inverse_transform([value])[0]
        else:
            decoded = value
        print(f"{label}: {decoded}")

# Uncomment this line to test input interface:
# predict_from_input()
