import pandas as pd
import os

# 1. Dynamically establish relative repository pathways
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "foresight_cleaned.csv.csv")
RISK_TRIAGE_PATH = os.path.join(BASE_DIR, "..", "data", "final_risk_triage.csv")

def get_filter_metadata():
    """Reads transactional files safely to establish dropdown ranges."""
    master = pd.read_csv(CLEANED_DATA_PATH)
    master.columns = [col.lower().strip() for col in master.columns]
    return list(master['region'].unique()), list(master['category'].unique())

def extract_and_filter_matrices(regions=None, categories=None):
    if not os.path.exists(CLEANED_DATA_PATH) or not os.path.exists(RISK_TRIAGE_PATH):
        return None, None

    master_df = pd.read_csv(CLEANED_DATA_PATH)
    master_df.columns = [col.lower().strip() for col in master_df.columns]
    master_df['date'] = pd.to_datetime(master_df['date'], format='mixed', dayfirst=True)

    triage_df = pd.read_csv(RISK_TRIAGE_PATH)
    triage_df.columns = [col.lower().strip() for col in triage_df.columns]

    if not regions:
        regions = list(master_df['region'].unique())
    if not categories:
        categories = list(master_df['category'].unique())

    filtered_master = master_df[(master_df['region'].isin(regions)) & (master_df['category'].isin(categories))]
    filtered_triage = triage_df[triage_df['category'].isin(categories)].copy()

    # Advanced Financial Metric Calculations
    filtered_triage['capital_tied_up'] = filtered_triage['total_on_hand'] * filtered_triage['unit_cost']
    velocity = filtered_triage['total_ml_forecast_units'] / 7.0
    filtered_triage['days_of_supply'] = filtered_triage['total_on_hand'] / (velocity + 1e-5)
    filtered_triage['days_of_supply'] = filtered_triage['days_of_supply'].clip(upper=365).round(1)

    return filtered_master, filtered_triage
