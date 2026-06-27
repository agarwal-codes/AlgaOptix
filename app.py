import streamlit as st
from datetime import datetime
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 1. RULE: Yeh pure code mein sabse pehla Streamlit command hona chahiye!
st.set_page_config(
    page_title="AI-Powered Algae Biofuel Predictor",
    layout="wide"
)

# 2. Naye machine learning models aur encoders ko load karein
biomass_model = joblib.load("biomass_model.pkl")
energy_model = joblib.load("energy_model.pkl")
species_encoder = joblib.load("species_encoder.pkl")
medium_encoder = joblib.load("medium_encoder.pkl")

from optimizer import get_best_conditions

# 3. Naye dataset ke 8 features ke naam aur naya biomass model use karenge
feature_names = [
    "Species",
    "Medium",
    "Temperature_C",
    "Light_umol_m2_s",
    "Nitrate_mg_L",
    "Phosphate_mg_L",
    "CO2_pct",
    "pH"
]

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": biomass_model.feature_importances_
})

importance_df = importance_df.sort_values(
    "Importance",
    ascending=False
)

# 4. Session state initialization (st.set_page_config ke humesha BAAD)
if "history" not in st.session_state:
    st.session_state.history = []

medium_data = {

    "TAP": {
        "pH": 7.0,
        "Nitrate": 10,
        "Phosphate": 2,
        "CO2": 0.04,
        "Description": "Natural freshwater source"
    },

    "Wastewater": {
        "pH": 7.5,
        "Nitrate": 45,
        "Phosphate": 15,
        "CO2": 1.0,
        "Description": "Nutrient-rich recycled wastewater"
    },

    "BG-11": {
        "pH": 7.1,
        "Nitrate": 150,
        "Phosphate": 40,
        "CO2": 2.0,
        "Description": "Standard microalgae laboratory medium"
    },

    "Bold's Basal Medium": {
        "pH": 6.8,
        "Nitrate": 120,
        "Phosphate": 30,
        "CO2": 2.0,
        "Description": "Widely used freshwater algae growth medium"
    },

    "f/2 Medium": {
        "pH": 8.0,
        "Nitrate": 75,
        "Phosphate": 15,
        "CO2": 2.0,
        "Description": "Marine microalgae cultivation medium"
    }

}

# species_conditions = {

#     "Chlorella vulgaris": {
#         "temperature": 28,
#         "light": 9000,
#         "nitrate": 80,
#         "phosphate": 20,
#         "co2": 5,
#         "ph": 7.0
#     },

#     "Spirulina platensis": {
#         "temperature": 32,
#         "light": 12000,
#         "nitrate": 100,
#         "phosphate": 25,
#         "co2": 6,
#         "ph": 8.5
#     },

#     "Scenedesmus obliquus": {
#         "temperature": 30,
#         "light": 10000,
#         "nitrate": 90,
#         "phosphate": 22,
#         "co2": 5,
#         "ph": 7.5
#     },

#     "Nannochloropsis": {
#         "temperature": 26,
#         "light": 11000,
#         "nitrate": 75,
#         "phosphate": 18,
#         "co2": 4,
#         "ph": 8.0
#     },

#     "Botryococcus braunii": {
#         "temperature": 25,
#         "light": 8000,
#         "nitrate": 60,
#         "phosphate": 15,
#         "co2": 4,
#         "ph": 7.2
#     }
# }

def predict_yields(species, medium, temperature, light, nitrate, phosphate, co2, ph):
    # Text ko numbers mein convert karna (Model ke liye)
    species_encoded = species_encoder.transform([species])[0]
    medium_encoded = medium_encoder.transform([medium])[0]
    
    input_data = pd.DataFrame({
        "Species": [species_encoded],
        "Medium": [medium_encoded],
        "Temperature_C": [temperature],
        "Light_umol_m2_s": [light],
        "Nitrate_mg_L": [nitrate],
        "Phosphate_mg_L": [phosphate],
        "CO2_pct": [co2],
        "pH": [ph]
    })

    # Donon naye models se prediction nikalna
    biomass = biomass_model.predict(input_data)[0]
    energy = energy_model.predict(input_data)[0]
    
    return biomass, energy

def generate_pdf_report(
    biomass,
    lipid,
    biofuel,
    temperature,
    light,
    nitrate,
    phosphate,
    co2,
    ph,
    water_type
):

    pdf_file = "AlgaOptix_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AlgaOptix Biofuel Yield Optimization Report",
            styles["Title"]
        )
    )
    st.caption(
    "Version 3.0 • Machine Learning Powered"
)

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Temperature: {temperature} °C",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Light Intensity: {light} Lux",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Nitrate: {nitrate} mg/L",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Phosphate: {phosphate} mg/L",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"CO₂: {co2} %",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"pH: {ph}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Medium: {water_type}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Biomass Yield: {biomass:.2f} g/L",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Lipid Yield: {lipid:.2f} g/L",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Biofuel Output: {biofuel:.2f}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return pdf_file

page="Prediction Dashboard"



if page == "Prediction Dashboard":

    st.title("AlgaOptix™ Biofuel Yield Optimizer")
    
    st.caption(
        "AI-Driven Algae Biomass & Biofuel Production Intelligence Platform"
    )

    st.markdown("""
    This system predicts algae biomass growth, lipid yield, energy output and biofuel production
    based on cultivation conditions.
    """)

    st.header("Input Parameters")

    col1, col2 = st.columns(2)

    # with col1:

    #     temperature = st.slider(
    #         "Temperature (°C)",
    #         15,
    #         40,
    #         28
    #     )

    #     light = st.slider(
    #         "Light Intensity (Lux)",
    #         1000,
    #         15000,
    #         8000
    #     )

    #     nitrate = st.slider(
    #         "Nitrate (mg/L)",
    #         0,
    #         100,
    #         50
    #     )

    # with col2:

    #     phosphate = st.slider(
    #         "Phosphate (mg/L)",
    #         0,
    #         50,
    #         20
    #     )

    #     co2 = st.slider(
    #         "CO₂ Concentration (%)",
    #         1,
    #         10,
    #         5
    #     )

    #     ph = st.slider(
    #         "pH",
    #         6.0,
    #         9.0,
    #         7.5
    #     )
    species = st.selectbox(
        "🧬 Select Algae Species",
        [
            "Chlorella vulgaris",
            "Spirulina platensis",
            "Scenedesmus obliquus",
            "Nannochloropsis sp.",
            "Botryococcus braunii"
        ]
    )
    water_type = st.selectbox(
        "Cultivation Medium",
        [
            "TAP",
            "Wastewater",
            "BG-11",
            "Bold's Basal Medium",
            "f/2 Medium"
        ]
    )
    current_medium = medium_data[water_type]

    st.info(
        f"""
    📋 Medium Profile

    {current_medium['Description']}

    • pH: {current_medium['pH']}

    • Nitrate: {current_medium['Nitrate']} mg/L

    • Phosphate: {current_medium['Phosphate']} mg/L

    • CO₂: {current_medium['CO2']} %
    """
    )

        # validation_score = 100

        # if temperature < 20 or temperature > 35:
        #     validation_score -= 20

        # if light < 5000:
        #     validation_score -= 20

        # if nitrate < 30:
        #     validation_score -= 20

        # if phosphate < 15:
        #     validation_score -= 20

        # if ph < 6.5 or ph > 8:
        #     validation_score -= 20

    # st.subheader("🧪 Cultivation Readiness")

    # st.progress(validation_score / 100)

    # st.caption(
    #     f"Cultivation Readiness Score: {validation_score}/100"
    # )

    if st.button("🚀 Predict and Optimize"):
    
       # Unpack the tuple directly into variables in the exact order returned by optimizer.py
        temperature, light, nitrate, phosphate, co2, ph = get_best_conditions(species, water_type)

        st.subheader("🧬 AI Recommended Conditions")

        st.info(
            f"""
        Temperature: {temperature} °C

        Light Intensity: {light} Lux

        Nitrate: {nitrate} mg/L

        Phosphate: {phosphate} mg/L

        CO₂: {co2} %

        pH: {ph}
        """
        )

        st.subheader("📈 Required Adjustments")

        nitrate_gap = nitrate - current_medium["Nitrate"]

        phosphate_gap = phosphate - current_medium["Phosphate"]

        co2_gap = co2 - current_medium["CO2"]

        ph_gap = ph - current_medium["pH"]

        if nitrate_gap > 0:
            st.write(
                f"➕ Increase Nitrate by {nitrate_gap:.1f} mg/L"
            )
        elif nitrate_gap < 0:
            st.write(
                f"➖ Decrease Nitrate by {abs(nitrate_gap):.1f} mg/L"
            )    

        if phosphate_gap > 0:
            st.write(
                f"➕ Increase Phosphate by {phosphate_gap:.1f} mg/L"
            )
        elif phosphate_gap < 0:
            st.write(
                f"➖ Decrease Phosphate by {abs(phosphate_gap):.1f} mg/L"
            )    

        if co2_gap > 0:
            st.write(
                f"➕ Increase CO₂ by {co2_gap:.1f}%"
            )
        elif co2_gap < 0:
            st.write(
                f"➖ Decrease CO₂ by {abs(co2_gap):.1f}%"
            )    

        if ph_gap > 0:
            st.write(
                f"➕ Increase pH by {ph_gap:.1f}"
            )

        elif ph_gap < 0:
            st.write(
                f"➖ Decrease pH by {abs(ph_gap):.1f}"
            )

        biomass, energy_output = predict_yields(
            species, water_type, temperature, light, nitrate, phosphate, co2, ph
        )
        
        # Population ab naye model ka part nahi hai, isliye metric update karein
        population = biomass * 1000000 # Just a placeholder multiplier if you still want to show population visually

        # if water_type == "Tap Water":
        #     biomass *= 1.00

        # elif water_type == "Municipal Wastewater":
        #     biomass *= 1.10

        # elif water_type == "BG-11":
        #     biomass *= 1.20

        # elif water_type == "Bold's Basal Medium":
        #     biomass *= 1.15

        # elif water_type == "f/2 Medium":
        #     biomass *= 1.18

        lipid = biomass * 0.25
        biofuel = lipid * 0.80
        
        # energy_output = biofuel * 37

        electricity_kwh = energy_output / 3.6

        # energy_score = min(
        #     int((energy_output / 60) * 100),
        #     100
        # )
        # sustainability = 60

        # if water_type == "Wastewater":
        #     sustainability += 20

        # if co2 >= 5:
        #     sustainability += 10

        # sustainability = min(sustainability, 100)

        success_message = st.success(
            "Prediction completed successfully."
        )
        import time

        time.sleep(2)

        success_message.empty()

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Biomass Yield",
            f"{biomass:.2f} g/L"
        )

        c2.metric(
            "Lipid Yield",
            f"{lipid:.2f} g/L"
        )

        c3.metric(
            "Biofuel Output",
            f"{biofuel:.2f} mL/g"
        )

        st.subheader("🤖 AI Model Prediction")

        st.metric(
            "Estimated Algae Population",
            f"{population:.0f} cells/mL"
        )

        st.metric(
            "Model Accuracy (R²)",
            "91.5%"
        )

        st.caption(
            "Model Version: Random Forest Regressor v1.0"
        )

    #     growth_rate = biomass / 14
    #     if biomass < 4:
    #         biomass_grade = "Low"

    #     elif biomass < 7:
    #         biomass_grade = "Moderate"

    #     else:
    #         biomass_grade = "High"

    #     c4.metric(
    #     "Growth Rate",
    #     f"{growth_rate:.2f} g/L/day"
    #     )

    #     c5.metric(
    #         "Biomass Grade",
    #         biomass_grade
    # )
        st.subheader("⚡ Energy Harvesting Potential")

        e1, e2, e3 = st.columns(3)

        e1.metric(
            "⚡ Energy Density",
            f"{energy_output:.2f} MJ/Kg"
        )

        e2.metric(
            "🔋 Electricity Equivalent",
            f"{electricity_kwh:.4f} kWh"
        )

        # e3.metric(
        #     "⚡ Energy Harvesting Score",
        #     f"{energy_score}/100"
        # )

        # st.progress(energy_score / 100)

        # if energy_score >= 80:
        #     st.success(
        #         "High energy harvesting potential detected."
        #     )

        # elif energy_score >= 50:
        #     st.warning(
        #         "Moderate energy harvesting potential."
        #     )

        # else:
        #     st.info(
        #         "Low energy harvesting potential."
        #     )

        # # 4. 14-Day Growth Curve (Jo aapne manga tha)
        # st.subheader("📈 14-Day Biomass Growth Curve")
        # growth_days = list(range(1, 15))
        # # Exponential growth simulation based on predicted biomass
        # growth_data = [biomass * (1.12 ** i) for i in range(14)]
        
        # df_growth = pd.DataFrame({"Day": growth_days, "Biomass": growth_data})
        # st.line_chart(df_growth.set_index("Day"))    
            
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "Timestamp": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Temperature": temperature,
            "Light": light,
            "Nitrate": nitrate,
            "Phosphate": phosphate,
            "CO2": co2,
            "pH": ph,
            "Medium": water_type,
            "Biomass": round(biomass,2),
            "Lipid": round(lipid,2),
            "Biofuel": round(biofuel,2)
        })

        # st.subheader("📈 Yield Assessment")

        # if biomass >= 6:
        #     st.success("Excellent Biomass Yield Potential")

        # elif biomass >= 4:
        #     st.warning("Good Biomass Yield Potential")

        # else:
        #     st.error("Low Biomass Yield Potential")

        # carbon_score = min(
        #     int((co2 * 10) + (sustainability * 0.3)),
        #     100
        # )

        # resource_score = min(
        #     int((nitrate + phosphate) / 1.5),
        #     100
        # )

        # economic_score = min(
        #     int(biofuel * 20),
        #     100
        # )

        # st.subheader("📊 Model Feature Importance")

        # st.bar_chart(
        #     importance_df.set_index("Feature")
        # )

        # st.subheader("📊 Executive Dashboard")

        # roi_score = round(
        #     biofuel * 15,
        #     2
        # )

        # productivity_score = round(
        #     biomass * 10,
        #     2
        # )

        # risk_score = round(
        #     100 - sustainability,
        #     2
        # )

        # m1, m2, m3 = st.columns(3)

        # m1.metric(
        #     "Carbon Impact",
        #     f"{carbon_score}/100"
        # )

        # m2.metric(
        #     "Resource Efficiency",
        #     f"{resource_score}/100"
        # )

        # m3.metric(
        #     "Economic Potential",
        #     f"{economic_score}/100"
        # )  

        # k1, k2, k3 = st.columns(3)

        # k1.metric(
        #     "ROI Index",
        #     roi_score
        # )

        # k2.metric(
        #     "Productivity Index",
        #     productivity_score
        # )

        # k3.metric(
        #     "Operational Risk",
        #     risk_score
        # ) 

        # st.subheader("📋 Executive Summary")

        # st.info(
        #     f"""
        #     Biomass Yield: {biomass:.2f} g/L

        #     Lipid Yield: {lipid:.2f} g/L

        #     Biofuel Output: {biofuel:.2f}
        #     Sustainability Score: {sustainability}/100

        #     Cultivation Medium: {water_type}
        #     """
        # ) 

        st.subheader("📈 14-Day Growth Simulation")

        growth = []

        current = biomass * 0.15

        for day in range(1, 15):
            growth.append(current)
            current = current * 1.12

        df = pd.DataFrame({
            "Day": list(range(1, 15)),
            "Biomass": growth
        })

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.plot(
            df["Day"],
            df["Biomass"],
            marker="o",
            linewidth=3
        )

        ax.set_title(
            "Projected Algae Biomass Growth Over 14 Days"
        )

        ax.set_xlabel(
            "Cultivation Days"
        )

        ax.set_ylabel(
            "Biomass Yield (g/L)"
        )

        ax.grid(True)

        ax.fill_between(
            df["Day"],
            df["Biomass"],
            alpha=0.3
        )

        st.pyplot(fig)

    #     st.subheader("📊 Scenario Comparison")

    #     tap_biomass = biomass
    #     waste_biomass = biomass
    #     nutrient_biomass = biomass

    #     comparison = pd.DataFrame({
    #         "Medium": [
    #             "Tap Water",
    #             "Wastewater",
    #             "Nutrient Rich Water"
    #         ],
    #         "Biomass (g/L)": [
    #             tap_biomass,
    #             waste_biomass,
    #             nutrient_biomass
    #         ],
    #         "Lipid (g/L)": [
    #             lipid,
    #             lipid * 1.10,
    #             lipid * 1.20
    #         ],
    #         "Biofuel": [
    #             biofuel,
    #             biofuel * 1.10,
    #             biofuel * 1.20
    #         ]
    # })

    #     st.dataframe(comparison)

    #     best_medium = comparison.loc[
    #         comparison["Biomass (g/L)"].idxmax(),
    #         "Medium"
    #     ]

    #     st.success(
    #         f"Best Performing Medium: {best_medium}"
    #     )

        # st.subheader("💰 Economic Projection")

        # price_per_unit = 120

        # revenue = biofuel * price_per_unit

        # st.metric(
        #     "Estimated Revenue",
        #     f"₹ {revenue:.2f}"
        # )

        # best_medium = comparison.loc[
        #     comparison["Biomass (g/L)"].idxmax(),
        #     "Medium"
        # ]

        # st.success(
        #     f"Best Performing Medium: {best_medium}"
        # )

        # st.subheader("🎯 Optimization Recommendations")

        # recommendations = []

        # if temperature < 28:
        #     recommendations.append(
        #         "Increase temperature by 2–4°C for higher growth rates."
        #     )

        # elif temperature > 32:
        #     recommendations.append(
        #         "Reduce temperature to avoid growth suppression."
        #     )

        # if light < 9000:
        #     recommendations.append(
        #         "Increase light intensity for improved photosynthesis."
        #     )

        # if nitrate < 60:
        #     recommendations.append(
        #         "Increase nitrate concentration to boost biomass."
        #     )

        # if phosphate < 25:
        #     recommendations.append(
        #         "Increase phosphate availability."
        #     )

        # if co2 < 6:
        #     recommendations.append(
        #         "Increase CO₂ concentration for higher productivity."
        #     )

        # if len(recommendations) == 0:
        #     recommendations.append(
        #         "Current cultivation conditions are close to optimal."
        #     )

        # for rec in recommendations:
        #     st.info(rec) 

        # optimization_gain = 18
        # future_biomass = biomass

        # st.subheader("🚀 Optimization Potential")

        # o1, o2 = st.columns(2)

        # o1.metric(
        #     "Projected Biomass",
        #     f"{future_biomass:.2f} g/L"
        # )

        # o2.metric(
        #     "Improvement",
        #     f"+{optimization_gain}%"
        # )  

        # st.subheader("⚠ Risk Assessment")
        # risk_score = 100

        # if temperature > 35:
        #     risk_score -= 20

        # if ph < 6.5 or ph > 8.5:
        #     risk_score -= 20

        # if co2 > 8:
        #     risk_score -= 15

        # if nitrate < 30:
        #     risk_score -= 15

        # st.metric(
        #     "Cultivation Risk Score",
        #     f"{risk_score}/100"
        # )

        # st.subheader("🌍 Sustainability Analysis")

        # if sustainability >= 85:
        #     st.success("Excellent Sustainability")

        # elif sustainability >= 70:
        #     st.warning("Good Sustainability")

        # else:
        #     st.error("Needs Optimization")

        # st.subheader("⚠ Operational Risk Assessment")

        # risk_factors = []

        # if temperature > 35:
        #     risk_factors.append(
        #         "Temperature stress risk"
        #     )

        # if ph < 6:
        #     risk_factors.append(
        #         "Acidic culture risk"
        #     )

        # if nitrate < 20:
        #     risk_factors.append(
        #         "Nutrient limitation risk"
        #     )

        # if co2 < 3:
        #     risk_factors.append(
        #         "Carbon limitation risk"
        #     )

        # if len(risk_factors) == 0:
        #     st.success(
        #         "No major cultivation risks detected."
        #     )

        # else:
        #     for risk in risk_factors:
        #         st.warning(risk)    

        st.subheader("📚 Experiment History")

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

        if len(st.session_state.history) > 1:

            trend_df = pd.DataFrame(
                st.session_state.history
            )

            # st.subheader("📈 Prediction Trend")

            # st.line_chart(
            #     trend_df["Biomass"]
            # )

        csv = history_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇ Download Experiment History",
            csv,
            "AlgaOptix_Experiment_History.csv",
            "text/csv"
        )    

        pdf_file = generate_pdf_report(
            biomass,
            lipid,
            biofuel,
            temperature,
            light,
            nitrate,
            phosphate,
            co2,
            ph,
            water_type
        )

        with open(pdf_file, "rb") as pdf:

            st.download_button(
                label="📥 Download Prediction Report",
                data=pdf,
                file_name="AlgaOptix_Prediction_Report.pdf",
                mime="application/pdf"
            )   

        # st.subheader("🌾 Harvest Recommendation")

        # if biomass >= 6:
        #     st.success(
        #         "Harvest Recommended: Biomass has reached commercially viable levels."
        #     )

        # elif biomass >= 4:
        #     st.warning(
        #         "Continue Cultivation for 3–5 more days."
        #     )

        # else:
        #     st.error(
        #         "Not Ready for Harvest."
        #     )
            
        report_df = pd.DataFrame({

            "Temperature":[temperature],
            "Light":[light],
            "Nitrate":[nitrate],
            "Phosphate":[phosphate],
            "CO2":[co2],
            "pH":[ph],
            "Medium":[water_type],
            "Biomass":[round(biomass,2)],
            "Lipid":[round(lipid,2)],
            "Biofuel":[round(biofuel,2)],
            "Energy": [round(energy_output,2)]
        })

     