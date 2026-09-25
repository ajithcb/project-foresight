import pandas as pd
import numpy as np
import os

def run_advanced_pipeline():
    print("🔄 Starting Phase 2 & 4: Data Engineering & Feature Engineering...")
    data_folder = r"C:\Users\ajith\Downloads\foresight\data"
    file_path = os.path.join(data_folder, "foresight_cleaned.csv.csv")
    
    if not os.path.exists(file_path):
        print(f"❌ File path error: {file_path} not found.")
        return None
        
    df = pd.read_csv(file_path)
    df.columns = [col.lower().strip() for col in df.columns]
    df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True)
    
    # Sort chronologically by item to avoid window mixing issues
    df = df.sort_values(by=['sku_id', 'date']).reset_index(drop=True)
    
    print("🛠 Engineering time-series lag and rolling features...")
    # 1. Historical Lookback Lags (What did we sell 1 day and 7 days ago?)
    df['lag_1_units'] = df.groupby('sku_id')['units_sold'].shift(1)
    df['lag_7_units'] = df.groupby('sku_id')['units_sold'].shift(7)
    
    # 2. Historical Rolling Averages (What was our average daily sales volume over the last week?)
    df['rolling_mean_7'] = df.groupby('sku_id')['units_sold'].transform(lambda x: x.shift(1).rolling(7).mean())
    df['rolling_std_7'] = df.groupby('sku_id')['units_sold'].transform(lambda x: x.shift(1).rolling(7).std())
    
    # 3. Categorical Encodings
    df['category_encoded'] = df['category'].astype('category').cat.codes
    
    # Handle NaN values introduced by historical lookback lag offsets safely
    df.fillna(0, inplace=True)
    
    print(f"✔ Features engineered. Matrix footprint shape: {df.shape}")
    return df

if __name__ == "__main__":
    run_advanced_pipeline()
