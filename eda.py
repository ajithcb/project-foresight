import pandas as pd
from pipeline import load_and_clean_data

def run_exploratory_analysis():
    # 1. Reuse the pipeline we just built to pull clean data into memory
    df = load_and_clean_data()
    if df is None:
        return
        
    print("\n==================================================")
    print("📈 RUNNING BUSINESS INTELLIGENCE INSIGHTS REPORT")
    print("==================================================")
    
    # 2. Extract Dataset Timeline Metrics
    start_date = df['date'].min().strftime('%Y-%m-%d')
    end_date = df['date'].max().strftime('%Y-%m-%d')
    print(f"🗓 Historical Data Range: From {start_date} to {end_date}")
    
    # 3. Calculate Category Financial Breakdown
    print("\n💰 Top Product Categories by Financial Revenue:")
    category_perf = df.groupby('category').agg(
        total_units_sold=('units_sold', 'sum'),
        total_revenue_generated=('revenue', 'sum')
    ).sort_values(by='total_revenue_generated', ascending=False)
    
    # Format numeric outputs cleanly for presentation logs
    for cat, row in category_perf.iterrows():
        print(f"   • {cat.title()}: {row['total_units_sold']:,} units sold | Revenue: ₹{row['total_revenue_generated']:,.2f}")
        
    # 4. Calculate Current Locked-Up Warehouse Capital
    print("\n📦 Total Physical Stock Posture Metrics:")
    # Calculate investment value per row: actual units * manufacturing unit cost
    df['inventory_valuation'] = df['on_hand'] * df['unit_cost']
    
    # We pull from the most recent historical snapshot date to see the true current state
    latest_date = df['date'].max()
    current_snapshot = df[df['date'] == latest_date]
    
    total_on_hand_units = current_snapshot['on_hand'].sum()
    total_capital_invested = current_snapshot['inventory_valuation'].sum()
    
    print(f"   • Latest Date Snapshot: {latest_date.strftime('%Y-%m-%d')}")
    print(f"   • Total Units Sitting in Warehouses: {total_on_hand_units:,} items")
    print(f"   • Total Capital Locked Up in Current Stock: ₹{total_capital_invested:,.2f}")
    print("==================================================")

if __name__ == "__main__":
    run_exploratory_analysis()
