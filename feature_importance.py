import joblib
import pandas as pd

model = joblib.load("algae_model.pkl")

importance = model.feature_importances_

features = [
    "Light",
    "Nitrate",
    "Iron",
    "Phosphate",
    "Temperature",
    "pH",
    "CO2"
]

df = pd.DataFrame({
    "Feature": features,
    "Importance": importance
})

print(df.sort_values(
    "Importance",
    ascending=False
))