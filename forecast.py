import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from pipeline import run_advanced_pipeline

def run_ml_forecasting():
    df = run_advanced_pipeline()
    if df is None:
        return None
        
    print("\n🌲 Starting Phase 5: Location-Aware Machine Learning Demand Forecasting...")
    
    # 1. Encode stores and regions alongside your categories
    df['store_encoded'] = df['store_id'].astype('category').cat.codes
    df['region_encoded'] = df['region'].astype('category').cat.codes
    
    # 2. Add local history features (shift lag based on both product and store locations)
    df['lag_1_local'] = df.groupby(['sku_id', 'store_id'])['units_sold'].shift(1)
    df['rolling_mean_7_local'] = df.groupby(['sku_id', 'store_id'])['units_sold'].transform(lambda x: x.shift(1).rolling(7).mean())
    df.fillna(0, inplace=True)
    
    # 3. Split chronologically to avoid future data leakage
    train_data = df[df['date'] < '2023-06-01'].copy()
    test_data = df[df['date'] >= '2023-06-01'].copy()
    
    # Define features including store and region tracking
    feature_cols = ['lag_1_units', 'lag_7_units', 'rolling_mean_7', 'rolling_std_7', 
                    'lag_1_local', 'rolling_mean_7_local',
                    'unit_cost', 'category_encoded', 'store_encoded', 'region_encoded']
    target_col = 'units_sold'
    
    X_train, y_train = train_data[feature_cols], train_data[target_col]
    X_test, y_test = test_data[feature_cols], test_data[target_col]
    
    print(f"📡 Training location-aware Random Forest on {len(X_train):,} transactional data rows...")
    model = RandomForestRegressor(n_estimators=30, max_depth=12, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Generate predictions
    test_data['ml_forecasted_units'] = model.predict(X_test)
    test_data['ml_forecasted_units'] = test_data['ml_forecasted_units'].clip(lower=0)
    
    # 4. Evaluate performance benchmarks
    base_abs_error = np.sum(np.abs(test_data['units_sold'] - test_data['demand_forecast']))
    ml_abs_error = np.sum(np.abs(test_data['units_sold'] - test_data['ml_forecasted_units']))
    total_actual_demand = np.sum(test_data['units_sold']) + 1e-5
    
    baseline_wape = (base_abs_error / total_actual_demand) * 100
    ml_wape = (ml_abs_error / total_actual_demand) * 100
    
    print("\n==================================================")
    print("📊 MODEL EVALUATION PERFORMANCE BENCHMARKS (FIXED)")
    print("==================================================")
    print(f"📉 Naive Baseline Model WAPE Error : {baseline_wape:.2f}%")
    print(f"🎯 Advanced ML Random Forest WAPE Error : {ml_wape:.2f}%")
    print(f"🌟 Net Accuracy Optimization Gain      : {(baseline_wape - ml_wape):.2f}% Improvement")
    print("==================================================")
    
    test_data.to_csv(r"C:\Users\ajith\Downloads\foresight\data\predictions_output.csv", index=False)
    print("💾 Location-aware predictions saved successfully.")
    return test_data

if __name__ == "__main__":
    run_ml_forecasting()
