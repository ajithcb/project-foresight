import pandas as pd
import numpy as np
import os

def run_strategic_risk_scoring():
    print("🎯 Starting Phase 6: Aggregate Warehouse Inventory Risk Scoring Engine...")
    pred_path = r"C:\Users\ajith\Downloads\foresight\data\predictions_output.csv"
    
    if not os.path.exists(pred_path):
        print("❌ Error: Run forecast.py first to establish data files.")
        return
        
    df = pd.read_csv(pred_path)
    latest_date = df['date'].max()
    current_state = df[df['date'] == latest_date].copy()
    
    # Collapse store records into single product totals for the central warehouse snapshot
    warehouse_grid = current_state.groupby(['sku_id', 'category', 'subcategory']).agg(
        total_on_hand=('on_hand', 'first'),
        total_on_order=('on_order', 'first'),
        reorder_trigger=('reorder_point', 'first'),
        unit_cost=('unit_cost', 'first'),
        total_ml_forecast_units=('ml_forecasted_units', 'sum')
    ).reset_index()
    
    triage_actions = []
    capital_at_stake = []
    
    for _, row in warehouse_grid.iterrows():
        total_available = row['total_on_hand'] + row['total_on_order']
        
        if total_available <= row['reorder_trigger']:
            triage_actions.append("Reorder Now")
            shortfall = max(0, row['reorder_trigger'] - total_available)
            capital_at_stake.append(shortfall * row['unit_cost'])
        elif row['total_on_hand'] > (row['total_ml_forecast_units'] * 5) and row['total_ml_forecast_units'] > 0:
            triage_actions.append("Markdown / Clear")
            excess = max(0, row['total_on_hand'] - row['total_ml_forecast_units'])
            capital_at_stake.append(excess * row['unit_cost'])
        else:
            triage_actions.append("Healthy")
            capital_at_stake.append(0.0)
            
    warehouse_grid['recommended_action'] = triage_actions
    warehouse_grid['rupee_impact_at_stake'] = capital_at_stake
    warehouse_grid['date'] = latest_date
    
    print("\n==================================================")
    print(f"📋 CORRECTED CENTRAL WAREHOUSE SNAPSHOT AUDIT REPORT")
    print("==================================================")
    print(warehouse_grid['recommended_action'].value_counts())
    print(f"\n💰 Cleaned Financial Risk Value Exposure: ₹{warehouse_grid['rupee_impact_at_stake'].sum():,.2f}")
    print("==================================================")
    
    warehouse_grid.to_csv(r"C:\Users\ajith\Downloads\foresight\data\final_risk_triage.csv", index=False)
    print("💾 Accurate risk matrices saved to final_risk_triage.csv")

if __name__ == "__main__":
    run_strategic_risk_scoring()
