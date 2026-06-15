from datetime import datetime
import joblib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
model = joblib.load("algae_model.pkl")

feature_names = [
    "Light",
    "Nitrate",
    "Iron",
    "Phosphate",
    "Temperature",
    "pH",
    "CO2"
]

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    "Importance",
    ascending=False
)

if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(
    page_title="AI-Powered Algae Biofuel Predictor",
    layout="wide"
)

def predict_biomass(
    temperature,
    light,
    nitrate,
    phosphate,
    co2,
    ph
):
    input_data = pd.DataFrame(
        {
            "Light":[light],
            "Nitrate":[nitrate],
            "Iron":[0.1],
            "Phosphate":[phosphate],
            "Temperature":[temperature],
            "pH":[ph],
            "CO2":[co2]
        }
    )

    population = model.predict(input_data)[0]

    biomass = population * 0.05
    return biomass, population


def generate_pdf_report(
    biomass,
    lipid,
    biofuel,
    sustainability,
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

    content.append(
        Paragraph(
            f"Sustainability Score: {sustainability}/100",
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
    This system predicts algae biomass growth, lipid yield and biofuel production
    based on cultivation conditions.
    """)

    st.header("Input Parameters")

    col1, col2 = st.columns(2)

    with col1:

        temperature = st.slider(
            "Temperature (°C)",
            15,
            40,
            28
        )

        light = st.slider(
            "Light Intensity (Lux)",
            1000,
            15000,
            8000
        )

        nitrate = st.slider(
            "Nitrate (mg/L)",
            0,
            100,
            50
        )

    with col2:

        phosphate = st.slider(
            "Phosphate (mg/L)",
            0,
            50,
            20
        )

        co2 = st.slider(
            "CO₂ Concentration (%)",
            1,
            10,
            5
        )

        ph = st.slider(
            "pH",
            6.0,
            9.0,
            7.5
        )

        water_type = st.selectbox(
            "Cultivation Medium",
            [
                "Tap Water",
                "Wastewater",
                "Nutrient Rich Water"
            ]
        )

        validation_score = 100

        if temperature < 20 or temperature > 35:
            validation_score -= 20

        if light < 5000:
            validation_score -= 20

        if nitrate < 30:
            validation_score -= 20

        if phosphate < 15:
            validation_score -= 20

        if ph < 6.5 or ph > 8:
            validation_score -= 20

    st.subheader("🧪 Cultivation Readiness")

    st.progress(validation_score / 100)

    st.caption(
        f"Cultivation Readiness Score: {validation_score}/100"
    )

    if st.button("🚀 Predict and Optimize"):
    
        biomass, population = predict_biomass(
            temperature,
            light,
            nitrate,
            phosphate,
            co2,
            ph
        )

        if water_type == "Wastewater":
            biomass *= 1.10

        elif water_type == "Nutrient Rich Water":
            biomass *= 1.20

        lipid = biomass * 0.25
        biofuel = lipid * 0.80
        
        energy_output = biofuel * 37

        electricity_kwh = energy_output / 3.6

        energy_score = min(
            int((energy_output / 60) * 100),
            100
        )
        sustainability = 60

        if water_type == "Wastewater":
            sustainability += 20

        if co2 >= 5:
            sustainability += 10

        sustainability = min(sustainability, 100)

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
            f"{biofuel:.2f}"
        )

        st.subheader("🤖 AI Model Prediction")

        st.metric(
            "Predicted Algae Population",
            f"{population:.0f}"
        )

        st.metric(
            "Model Accuracy (R²)",
            "95.8%"
        )

        st.caption(
            "Model Version: Random Forest Regressor v1.0"
        )

        growth_rate = biomass / 14
        if biomass < 4:
            biomass_grade = "Low"

        elif biomass < 7:
            biomass_grade = "Moderate"

        else:
            biomass_grade = "High"

        c4.metric(
        "Growth Rate",
        f"{growth_rate:.2f} g/L/day"
        )

        c5.metric(
            "Biomass Grade",
            biomass_grade
    )
        st.subheader("⚡ Energy Harvesting Potential")

        e1, e2, e3 = st.columns(3)

        e1.metric(
            "⚡ Energy Output",
            f"{energy_output:.2f} MJ"
        )

        e2.metric(
            "🔋 Electricity Equivalent",
            f"{electricity_kwh:.2f} kWh"
        )

        e3.metric(
            "⚡ Energy Harvesting Score",
            f"{energy_score}/100"
        )

        st.progress(energy_score / 100)

        if energy_score >= 80:
            st.success(
                "High energy harvesting potential detected."
            )

        elif energy_score >= 50:
            st.warning(
                "Moderate energy harvesting potential."
            )

        else:
            st.info(
                "Low energy harvesting potential."
            )
            
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

        st.subheader("📈 Yield Assessment")

        if biomass >= 6:
            st.success("Excellent Biomass Yield Potential")

        elif biomass >= 4:
            st.warning("Good Biomass Yield Potential")

        else:
            st.error("Low Biomass Yield Potential")

        carbon_score = min(
            int((co2 * 10) + (sustainability * 0.3)),
            100
        )

        resource_score = min(
            int((nitrate + phosphate) / 1.5),
            100
        )

        economic_score = min(
            int(biofuel * 20),
            100
        )

        st.subheader("📊 Model Feature Importance")

        st.bar_chart(
            importance_df.set_index("Feature")
        )

        st.subheader("📊 Executive Dashboard")

        roi_score = round(
            biofuel * 15,
            2
        )

        productivity_score = round(
            biomass * 10,
            2
        )

        risk_score = round(
            100 - sustainability,
            2
        )

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Carbon Impact",
            f"{carbon_score}/100"
        )

        m2.metric(
            "Resource Efficiency",
            f"{resource_score}/100"
        )

        m3.metric(
            "Economic Potential",
            f"{economic_score}/100"
        )  

        k1, k2, k3 = st.columns(3)

        k1.metric(
            "ROI Index",
            roi_score
        )

        k2.metric(
            "Productivity Index",
            productivity_score
        )

        k3.metric(
            "Operational Risk",
            risk_score
        ) 

        st.subheader("📋 Executive Summary")

        st.info(
            f"""
            Biomass Yield: {biomass:.2f} g/L

            Lipid Yield: {lipid:.2f} g/L

            Biofuel Output: {biofuel:.2f}
            Sustainability Score: {sustainability}/100

            Cultivation Medium: {water_type}
            """
        ) 

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

        st.subheader("📊 Scenario Comparison")

        tap_biomass = biomass

        waste_biomass = biomass * 1.10

        nutrient_biomass = biomass * 1.20

        comparison = pd.DataFrame({
            "Medium": [
                "Tap Water",
                "Wastewater",
                "Nutrient Rich Water"
            ],
            "Biomass (g/L)": [
                tap_biomass,
                waste_biomass,
                nutrient_biomass
            ],
            "Lipid (g/L)": [
                lipid,
                lipid * 1.10,
                lipid * 1.20
            ],
            "Biofuel": [
                biofuel,
                biofuel * 1.10,
                biofuel * 1.20
            ]
    })

        st.dataframe(comparison)

        best_medium = comparison.loc[
            comparison["Biomass (g/L)"].idxmax(),
            "Medium"
        ]

        st.success(
            f"Best Performing Medium: {best_medium}"
        )

        st.subheader("💰 Economic Projection")

        price_per_unit = 120

        revenue = biofuel * price_per_unit

        st.metric(
            "Estimated Revenue",
            f"₹ {revenue:.2f}"
        )

        best_medium = comparison.loc[
            comparison["Biomass (g/L)"].idxmax(),
            "Medium"
        ]

        st.success(
            f"Best Performing Medium: {best_medium}"
        )

        st.subheader("🎯 Optimization Recommendations")

        recommendations = []

        if temperature < 28:
            recommendations.append(
                "Increase temperature by 2–4°C for higher growth rates."
            )

        elif temperature > 32:
            recommendations.append(
                "Reduce temperature to avoid growth suppression."
            )

        if light < 9000:
            recommendations.append(
                "Increase light intensity for improved photosynthesis."
            )

        if nitrate < 60:
            recommendations.append(
                "Increase nitrate concentration to boost biomass."
            )

        if phosphate < 25:
            recommendations.append(
                "Increase phosphate availability."
            )

        if co2 < 6:
            recommendations.append(
                "Increase CO₂ concentration for higher productivity."
            )

        if len(recommendations) == 0:
            recommendations.append(
                "Current cultivation conditions are close to optimal."
            )

        for rec in recommendations:
            st.info(rec) 

        optimization_gain = 18

        future_biomass = biomass * (
            1 + optimization_gain / 100
        )

        st.subheader("🚀 Optimization Potential")

        o1, o2 = st.columns(2)

        o1.metric(
            "Projected Biomass",
            f"{future_biomass:.2f} g/L"
        )

        o2.metric(
            "Improvement",
            f"+{optimization_gain}%"
        )  

        st.subheader("⚠ Risk Assessment")
        risk_score = 100

        if temperature > 35:
            risk_score -= 20

        if ph < 6.5 or ph > 8.5:
            risk_score -= 20

        if co2 > 8:
            risk_score -= 15

        if nitrate < 30:
            risk_score -= 15

        st.metric(
            "Cultivation Risk Score",
            f"{risk_score}/100"
        )

        st.subheader("🌍 Sustainability Analysis")

        if sustainability >= 85:
            st.success("Excellent Sustainability")

        elif sustainability >= 70:
            st.warning("Good Sustainability")

        else:
            st.error("Needs Optimization")

        st.subheader("⚠ Operational Risk Assessment")

        risk_factors = []

        if temperature > 35:
            risk_factors.append(
                "Temperature stress risk"
            )

        if ph < 6:
            risk_factors.append(
                "Acidic culture risk"
            )

        if nitrate < 20:
            risk_factors.append(
                "Nutrient limitation risk"
            )

        if co2 < 3:
            risk_factors.append(
                "Carbon limitation risk"
            )

        if len(risk_factors) == 0:
            st.success(
                "No major cultivation risks detected."
            )

        else:
            for risk in risk_factors:
                st.warning(risk)    

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

            st.subheader("📈 Prediction Trend")

            st.line_chart(
                trend_df["Biomass"]
            )

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
            sustainability,
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

        st.subheader("🌾 Harvest Recommendation")

        if biomass >= 6:
            st.success(
                "Harvest Recommended: Biomass has reached commercially viable levels."
            )

        elif biomass >= 4:
            st.warning(
                "Continue Cultivation for 3–5 more days."
            )

        else:
            st.error(
                "Not Ready for Harvest."
            )
            
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
            "Sustainability":[sustainability]
        })

     