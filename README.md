## 🌐 Live Demo

https://algaoptix-ibpl.streamlit.app

# 🌱 AlgaOptix™

### AI-Powered Algae Biofuel Yield & Energy Optimization System

AlgaOptix™ is an AI-powered decision support system that optimizes algae cultivation for sustainable biofuel production. The application predicts biomass growth, lipid yield, biofuel production, and energy potential while recommending optimal cultivation conditions for different algae species and growth media.

Designed as an interdisciplinary engineering project, AlgaOptix combines Machine Learning, Data Science, Environmental Engineering, and Renewable Energy into a single interactive Streamlit application.

---

# 🚀 Features

* 🌿 Multiple algae species selection
* 🧪 Multiple cultivation media support
* 🤖 AI-recommended cultivation conditions
* 📈 Biomass prediction
* 🛢 Lipid yield estimation
* ⛽ Biofuel production estimation
* ⚡ Energy output prediction using Machine Learning
* 🔧 Required cultivation adjustments
* 📊 Growth visualization
* 📄 PDF report generation
* 🕒 Experiment history tracking
* 🎨 Modern interactive Streamlit dashboard

---

# 🧠 Machine Learning Models

The project uses multiple trained machine learning models.

## 1. Biomass Prediction Model

**Purpose**

Predict algae biomass under optimized cultivation conditions.

**Inputs**

* Species
* Medium
* Temperature
* Light Intensity
* Nitrate
* Phosphate
* CO₂
* pH

**Output**

* Biomass Yield (g/L)

---

## 2. Energy Prediction Model

**Purpose**

Predict energy obtainable from algae-derived biofuel.

**Algorithm**

Random Forest Regressor

**Model Performance**

* High predictive accuracy (R² > 0.90)

**Output**

* Energy Output (MJ/kg)

---

# 📂 Dataset

The project uses a curated algae cultivation dataset containing:

* Species information
* Cultivation media
* Temperature
* Light intensity
* Nutrient concentrations
* CO₂ levels
* pH
* Biomass
* Lipid percentage
* Biofuel yield
* Energy output

The dataset combines literature-derived cultivation data with scientifically constrained modeled data to improve prediction coverage while maintaining biological realism.

---

# ⚙️ Technology Stack

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Matplotlib
* ReportLab

---

# 🏗 Project Workflow

```text
Species Selection
        │
        ▼
Cultivation Medium Selection
        │
        ▼
AI Optimization Engine
        │
        ▼
Recommended Cultivation Conditions
        │
        ▼
Required Parameter Adjustments
        │
        ▼
Biomass Prediction
        │
        ▼
Lipid Yield Estimation
        │
        ▼
Biofuel Yield Estimation
        │
        ▼
Energy Output Prediction
        │
        ▼
Electricity Equivalent
        │
        ▼
PDF Report Generation
```

---

# 📁 Project Structure

```
AlgaOptix/
│
├── app.py
├── optimizer.py
├── requirements.txt
├── README.md
│
├── biomass_model.pkl
├── energy_model.pkl
├── species_encoder.pkl
├── medium_encoder.pkl
│
├── datasets/
│   └── AlgaOptix_Dataset_700rows.csv
│
├── assets/
```

---

# ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/agarwal-codes/AlgaOptix.git
```

Move into the project directory:

```bash
cd AlgaOptix
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

# 📊 Future Enhancements

* Microbial Fuel Cell (MFC) energy estimation
* Carbon sequestration analysis
* Multi-objective AI optimization
* IoT-based real-time cultivation monitoring
* Deep Learning prediction models
* Cloud database integration
* User authentication and experiment management
* Industrial-scale cultivation planning

---

# 🌍 Applications

* Renewable Energy Research
* Sustainable Biofuel Production
* Environmental Engineering
* Smart Algae Cultivation
* Academic Research
* Educational Demonstrations

---

# 👨‍💻 Authors

**Divyansh Agarwal**

First-Year Engineering Student

Interests:

* Artificial Intelligence
* Machine Learning
* Renewable Energy
* Environmental Technology
* Sustainable Engineering

---

# 📜 License

This project is developed for educational and research purposes.
