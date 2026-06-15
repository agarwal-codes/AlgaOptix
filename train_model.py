import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

# Load dataset
df = pd.read_csv("datasets/algeas.csv")

# Features
X = df[
    [
        "Light",
        "Nitrate",
        "Iron",
        "Phosphate",
        "Temperature",
        "pH",
        "CO2"
    ]
]

# Target
y = df["Population"]

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
predictions = model.predict(X_test)

score = r2_score(y_test, predictions)

print("\nModel Accuracy (R²):")
print(score)

# Save model
joblib.dump(
    model,
    "algae_model.pkl"
)

print("\nModel saved successfully.")