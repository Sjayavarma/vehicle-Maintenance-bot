import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ✅ Create the "model" folder if it doesn't exist
model_dir = "model"
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Sample dataset for training (Engine Temperature, Battery Health, Tire Pressure)
data = {
    "Engine_Temperature": np.random.randint(70, 120, 100),
    "Battery_Health": np.random.randint(40, 100, 100),
    "Tire_Pressure": np.random.randint(20, 50, 100),
    "Maintenance_Needed": np.random.choice(["No Maintenance", "Check Soon", "Immediate Maintenance"], 100)
}

df = pd.DataFrame(data)

# Convert target labels to numerical values
df["Maintenance_Needed"] = df["Maintenance_Needed"].astype("category").cat.codes

# Split dataset
X = df.drop("Maintenance_Needed", axis=1)
y = df["Maintenance_Needed"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Save model
model_path = os.path.join(model_dir, "predictive_maintenance_model.pkl")
joblib.dump(model, model_path)

print("✅ Model trained and saved successfully!")
