# 📈 Project FORESIGHT
> AI-Powered Demand Forecasting & Supply Chain Triage Engine

An enterprise-ready data science implementation built to optimize inventory availability, model localized velocity trends, and flag active portfolio capital liabilities for NorthBay Living [0.1.1, ID].

📊 **Live Production Dashboard Hub**: [project-foresight-1.streamlit.app](https://streamlit.app)

---

## 📂 System Directory Structure
```text
project-foresight/
│
├── app.py                 # Core Dashboard Web Application Router
├── dashboard_pipeline.py  # Data Processing & Filtration Engine
├── tab_operational.py     # Tab 1: Supply Triage, Sims, & PO Downloader
├── tab_commercial.py      # Tab 2: Gross Sales Performance Analysis
├── tab_features.py        # Tab 3: Price Elasticity & Weather Analytics
├── tab_summary.py         # Tab 4: Final Executive Summary & Audit Memo
│
├── foresight_cleaned.csv.csv  # Raw Master Ledger (73,100 Rows)
├── final_risk_triage.csv      # Compiled Operational Scores Snapshot
├── predictions_output.csv     # Cached Machine Learning Inferences
└── requirements.txt       # Active Cloud Dependencies Ecosystem
```

## 🚀 Deployed Architecture Features
*   **🎯 Tab 1: Operational Risk Matrix**: Implements interactive what-if simulation sliders, a clearance markdown margin calculator, and an automated supplier Excel Purchase Order (.xlsx) spreadsheet generator.
*   **📈 Tab 2: Commercial Sales Intelligence**: Deploys responsive Plotly line charts tracking gross revenues, regional volume shares, and sales run-rates over time.
*   **🌦 Tab 3: Market Features Analytics**: A visualization layer modeling external weather variables, seasonal discount spreads, and competitive price elasticity vectors.
*   **📝 Tab 4: Final Executive Summary**: A built-in phase-by-phase financial summary and strategic data memo for rapid leadership evaluations.

## 💻 Local Execution Playbook

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Execute Background Models**:
   ```bash
   python forecast.py
   python risk.py
   ```
3. **Launch Local Application Server**:
   ```bash
   streamlit run app.py
   ```
