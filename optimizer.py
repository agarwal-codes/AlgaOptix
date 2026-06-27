
# import pandas as pd
# import joblib
# import itertools

# model = joblib.load("energy_model.pkl")
# species_encoder = joblib.load("species_encoder.pkl")
# medium_encoder = joblib.load("medium_encoder.pkl")


# def get_best_conditions(species, medium):

#     species_encoded = species_encoder.transform(
#         [species]
#     )[0]

#     medium_encoded = medium_encoder.transform(
#         [medium]
#     )[0]

#     temperatures = [25, 28, 31, 34]

#     lights = [5000, 8000, 12000, 15000]

#     nitrates = [50, 100, 150, 200]

#     phosphates = [10, 20, 30, 40]

#     co2s = [1, 3, 5, 7]

#     phs = [6.5, 7.0, 8.0, 9.0]

#     best_energy = -999

#     best_conditions = None

#     for temp, light, nitrate, phosphate, co2, ph in itertools.product(
#         temperatures,
#         lights,
#         nitrates,
#         phosphates,
#         co2s,
#         phs
#     ):

#         sample = pd.DataFrame(
#             [[
#                 species_encoded,
#                 medium_encoded,
#                 temp,
#                 light,
#                 nitrate,
#                 phosphate,
#                 co2,
#                 ph
#             ]],
#             columns=[
#                 "Species",
#                 "Medium",
#                 "Temperature_C",
#                 "Light_umol_m2_s",
#                 "Nitrate_mg_L",
#                 "Phosphate_mg_L",
#                 "CO2_pct",
#                 "pH"
#             ]
#         )

#         energy = model.predict(sample)[0]

#         if energy > best_energy:

#             best_energy = energy

#             best_conditions = (
#                 temp,
#                 light,
#                 nitrate,
#                 phosphate,
#                 co2,
#                 ph
#             )

#     return {
#         "temperature": best_conditions[0],
#         "light": best_conditions[1],
#         "nitrate": best_conditions[2],
#         "phosphate": best_conditions[3],
#         "co2": best_conditions[4],
#         "ph": best_conditions[5],
#         "energy": best_energy
#     }
# import pandas as pd
# import joblib
# import itertools
# import numpy as np

# # Models aur Encoders ko load karein
# model = joblib.load("energy_model.pkl")
# species_encoder = joblib.load("species_encoder.pkl")
# medium_encoder = joblib.load("medium_encoder.pkl")

# def get_best_conditions(species, medium):
#     # Species aur Medium ko encode karein
#     species_encoded = species_encoder.transform([species])[0]
#     medium_encoded = medium_encoder.transform([medium])[0]

#     # Saari possible ranges
#     temperatures = [25, 28, 31, 34]
#     lights = [5000, 8000, 12000, 15000]
#     nitrates = [50, 100, 150, 200]
#     phosphates = [10, 20, 30, 40]
#     co2s = [1, 3, 5, 7]
#     phs = [6.5, 7.0, 8.0, 9.0]

#     # 1. LOOP HATAKAR: Ek hi baar mein saare 4096 combinations ki list banayein
#     combinations = list(itertools.product(temperatures, lights, nitrates, phosphates, co2s, phs))
    
#     # 2. Ek single bada DataFrame banayein saari rows ke saath (Fast!)
#     df_comb = pd.DataFrame(combinations, columns=[
#         "Temperature_C", "Light_umol_m2_s", "Nitrate_mg_L", "Phosphate_mg_L", "CO2_pct", "pH"
#     ])
    
#     # Encoded columns ko sahi positions par insert karein
#     df_comb.insert(0, "Species", species_encoded)
#     df_comb.insert(1, "Medium", medium_encoded)
    
#     # Columns ka order model ke hisab se match karein
#     df_comb = df_comb[[
#         "Species", "Medium", "Temperature_C", "Light_umol_m2_s", 
#         "Nitrate_mg_L", "Phosphate_mg_L", "CO2_pct", "pH"
#     ]]

#     # 3. BATCH PREDICTION: Saare 4096 rows ko ek hi jhatke mein predict karein (Super Fast!)
#     predictions = model.predict(df_comb)
    
#     # Sabse zyada energy output waali row ka index nikalen
#     best_idx = np.argmax(predictions)
#     best_row = df_comb.iloc[best_idx]
    
#     # Best conditions return karein
#     return (
#         float(best_row["Temperature_C"]),
#         float(best_row["Light_umol_m2_s"]),
#         float(best_row["Nitrate_mg_L"]),
#         float(best_row["Phosphate_mg_L"]),
#         float(best_row["CO2_pct"]),
#         float(best_row["pH"])
#     )
import pandas as pd
import joblib
import itertools
import numpy as np

# Models aur Encoders ko load karein
model = joblib.load("energy_model.pkl")
species_encoder = joblib.load("species_encoder.pkl")
medium_encoder = joblib.load("medium_encoder.pkl")

def get_best_conditions(species="Chlorella vulgaris", medium="TAP"):
    # SMART CHECK: Agar app.py ne Species ki jagah Medium bhej diya hai, toh swap karein
    if species in medium_encoder.classes_:
        species, medium = medium, species

    # Safe check: Agar species abhi bhi valid nahi hai toh default set karein
    if species not in species_encoder.classes_:
        species = "Chlorella vulgaris"

    # Safe check: Agar medium valid nahi hai toh default set karein
    if medium not in medium_encoder.classes_:
        medium = "TAP"

    # Species aur Medium ko encode karein
    species_encoded = species_encoder.transform([species])[0]
    medium_encoded = medium_encoder.transform([medium])[0]

    # Saari possible ranges
    temperatures = [25, 28, 31, 34]
    lights = [5000, 8000, 12000, 15000]
    nitrates = [50, 100, 150, 200]
    phosphates = [10, 20, 30, 40]
    co2s = [1, 3, 5, 7]
    phs = [6.5, 7.0, 8.0, 9.0]

    # Ek hi baar mein saare 4096 combinations ki list banayein
    combinations = list(itertools.product(temperatures, lights, nitrates, phosphates, co2s, phs))
    
    # Ek single naya DataFrame banayein saari rows ke saath
    df_comb = pd.DataFrame(combinations, columns=[
        "Temperature_C", "Light_umol_m2_s", "Nitrate_mg_L", "Phosphate_mg_L", "CO2_pct", "pH"
    ])
    
    # Encoded columns ko sahi positions par insert karein
    df_comb.insert(0, "Species", species_encoded)
    df_comb.insert(1, "Medium", medium_encoded)
    
    # Columns ka order model ke hisab se match karein
    df_comb = df_comb[[
        "Species", "Medium", "Temperature_C", "Light_umol_m2_s", 
        "Nitrate_mg_L", "Phosphate_mg_L", "CO2_pct", "pH"
    ]]

    # Batch prediction (Super Fast!)
    predictions = model.predict(df_comb)
    
    # Sabse zyada energy output waali row ka index nikalen
    best_idx = np.argmax(predictions)
    best_row = df_comb.iloc[best_idx]
    
    # Best conditions return karein
    return (
        float(best_row["Temperature_C"]),
        float(best_row["Light_umol_m2_s"]),
        float(best_row["Nitrate_mg_L"]),
        float(best_row["Phosphate_mg_L"]),
        float(best_row["CO2_pct"]),
        float(best_row["pH"])
    )