import pandas as pd
import os

CLEANED_DATA_PATH = r"C:\Users\ajith\Downloads\foresight\data\foresight_cleaned.csv.csv"
RISK_TRIAGE_PATH = r"C:\Users\ajith\Downloads\foresight\data\final_risk_triage.csv"

def load_and_filter_data(selected_regions=None, selected_categories=None):
    """
    Ingests data tables, unifies naming conventions, and filters data 
    cross-functionally to drive front-end web components.
    """
    if not os.path.exists(CLEANED_DATA_PATH) or not os.path.exists(RISK_TRIAGE_PATH):
        return None, None

    # Load master historical records
    master_df = pd.read_csv(CLEANED_DATA_PATH)
    master_df.columns = [col.lower().strip() for col in master_df.columns]
    master_df['date'] = pd.to_datetime(master_df['date'], format='mixed', dayfirst=True)

    # Load aggregated risk portfolio profiles
    triage_df = pd.read_csv(RISK_TRIAGE_PATH)
    triage_df.columns = [col.lower().strip() for col in triage_df.columns]

    # Handle fallback conditions if selections are empty
    if not selected_regions:
        selected_regions = list(master_df['region'].unique())
    if not selected_categories:
        selected_categories = list(master_df['category'].unique())

    # Apply global filtering rules
    filtered_master = master_df[
        (master_df['region'].isin(selected_regions)) & 
        (master_df['category'].isin(selected_categories))
    ]
    
    filtered_triage = triage_df[triage_df['category'].isin(selected_categories)]

    return filtered_master, filtered_triage
