import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

def render_operational_matrix_tab(filtered_triage):
    st.markdown("#### 🏬 Central Warehouse Triage Control Panel")
    st.markdown("---")
    
    # 1. Advanced Planning Scenario Simulator Controls
    st.markdown("##### ⚙️ Simulation Modifiers: What-If Optimization Scenarios")
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        holding_cost_rate = st.slider("Annual Warehouse Holding Cost Rate (% of Product Cost):", min_value=5, max_value=40, value=18)
    with sim_col2:
        target_safety_days = st.slider("Target Safety Stock Cushion Runway (Days):", min_value=7, max_value=60, value=30)
        
    sim_triage = filtered_triage.copy()
    sim_triage['annual_holding_cost'] = sim_triage['capital_tied_up'] * (holding_cost_rate / 100)
    
    # 2. Markdown Optimizer
    st.markdown("---")
    st.markdown("##### 📉 Dead-Stock Markdown & Margin Clearance Optimizer")
    overstock_items = sim_triage[sim_triage['recommended_action'] == "Markdown / Clear"]
    if not overstock_items.empty:
        clearance_discount = st.slider("Simulate Clearance Discount Rate (%):", min_value=10, max_value=70, value=30)
        recovered_cash = overstock_items['capital_tied_up'].sum() * (1 - (clearance_discount / 100))
        margin_hit = overstock_items['capital_tied_up'].sum() * (clearance_discount / 100)
        
        md_c1, md_c2 = st.columns(2)
        md_c1.metric("Projected Working Capital Recovered", f"₹{recovered_cash:,.2f}")
        md_c2.metric("Projected Gross Margin Liquidation Hit", f"₹{margin_hit:,.2f}", delta="- Margin Loss", delta_color="inverse")
    else:
        st.success("✅ Operational Excellence: Zero dead-stock overstock anomalies detected inside profiles.")

    # 3. Interactive Plotly Analytical Charts
    st.markdown("---")
    st.markdown("##### 📊 Interactive Risk Matrix Profiles")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig_exposure = px.bar(
            sim_triage.groupby('category')['rupee_impact_at_stake'].sum().reset_index(),
            x='category', y='rupee_impact_at_stake',
            labels={'category': 'Product Category', 'rupee_impact_at_stake': 'Exposure Value (₹)'},
            title='Net Financial Liability Exposure By Category', color_discrete_sequence=['#FF4B4B']
        )
        fig_exposure.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_exposure, use_container_width=True)
    with chart_col2:
        action_mix = sim_triage['recommended_action'].value_counts().reset_index()
        action_mix.columns = ['Triage Status', 'Volume']
        fig_pie = px.pie(action_mix, values='Volume', names='Triage Status', title='Warehouse Strategy Allocation Mix', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    # 4. Automated PO Spreadsheet Generation
    st.markdown("---")
    st.markdown("##### 📦 Automated Procurement Hub & Order Processing")
    reorder_items = sim_triage[sim_triage['recommended_action'] == "Reorder Now"].copy()
    if not reorder_items.empty:
        daily_velocity = reorder_items['total_ml_forecast_units'] / 7.0
        target_stock_units = (daily_velocity * target_safety_days).round(0)
        reorder_items['suggested_order_quantity'] = (target_stock_units - (reorder_items['total_on_hand'] + reorder_items['total_on_order'])).clip(lower=0).astype(int)
        reorder_items['purchase_order_cost'] = reorder_items['suggested_order_quantity'] * reorder_items['unit_cost']
        po_sheet = reorder_items[reorder_items['suggested_order_quantity'] > 0][['sku_id', 'category', 'total_on_hand', 'suggested_order_quantity', 'purchase_order_cost']]
        
        st.dataframe(po_sheet, width="stretch", hide_index=True)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            po_sheet.to_excel(writer, index=False, sheet_name='NorthBay_Replenishment_PO')
        st.download_button(
            label="📥 Download Official Supplier Purchase Order (.xlsx)",
            data=buffer.getvalue(), file_name="NorthBay_Replenishment_PO.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.markdown("---")
    st.write("##### 🔍 Master Operational Inventory Fleet Ledger")
    st.dataframe(
        sim_triage[['sku_id', 'category', 'total_on_hand', 'days_of_supply', 'capital_tied_up', 'recommended_action', 'rupee_impact_at_stake']],
        column_config={
            "sku_id": "SKU Identifier", "category": "Product Category", "total_on_hand": "Physical Stock",
            "days_of_supply": "Runway (Days of Supply)", "capital_tied_up": "Capital Tied-Up (₹)",
            "recommended_action": "Triage Action Group", "rupee_impact_at_stake": st.column_config.NumberColumn("Exposure Risk (₹)", format="₹%.2f")
        },
        width="stretch", hide_index=True
    )

def render_commercial_sales_tab(filtered_master):
    st.markdown("#### 📈 Enterprise Revenue & Velocity Performance Channels")
    
    total_sales_units = filtered_master['units_sold'].sum()
    total_gross_rev = filtered_master['revenue'].sum()
    avg_margin = ((filtered_master['revenue'] - (filtered_master['units_sold'] * filtered_master['unit_cost'])).sum() / (total_gross_rev + 1e-5)) * 100
    
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(f'<div class="metric-box" style="border-left-color: #6f42c1;"><div class="metric-box-title">Gross Volume Dispatched</div><div class="metric-box-value">{total_sales_units:,} units</div></div>', unsafe_allow_html=True)
    with mc2:
        st.markdown(f'<div class="metric-box" style="border-left-color: #e83e8c;"><div class="metric-box-title">Total Earned Gross Revenue</div><div class="metric-box-value">₹{total_gross_rev:,.2f}</div></div>', unsafe_allow_html=True)
    with mc3:
        st.markdown(f'<div class="metric-box" style="border-left-color: #17a2b8;"><div class="metric-box-title">Calculated Gross Margin (%)</div><div class="metric-box-value">{avg_margin:.2f}% Margin</div></div>', unsafe_allow_html=True)
        
    st.write("##### 🗓 Historical Sales Revenue Timeline Run-Rate")
    time_series = filtered_master.groupby('date')['revenue'].sum().reset_index()
    fig_line = px.line(time_series, x='date', y='revenue', title='Gross Dispatched Revenue Timeline Volume', color_discrete_sequence=['#6f42c1'])
    st.plotly_chart(fig_line, use_container_width=True)
    
    sc1, sc2 = st.columns(2)
    with sc1:
        st.write("##### 🗺 Regional Revenue Performance Share")
        reg_rev = filtered_master.groupby('region')['revenue'].sum().reset_index()
        fig_reg = px.bar(reg_rev, x='region', y='revenue', color='revenue', color_continuous_scale='Purples')
        st.plotly_chart(fig_reg, use_container_width=True)
    with sc2:
        st.write("##### 🛍 Category Volume Contribution Profiles")
        cat_units = filtered_master.groupby('category')['units_sold'].sum().reset_index()
        fig_cat = px.bar(cat_units, x='category', y='units_sold', color='units_sold', color_continuous_scale='Magma')
        st.plotly_chart(fig_cat, use_container_width=True)

def render_market_features_tab(filtered_master):
    st.markdown("#### 🌦 External Features & Predictive Model Dynamics")
    
    fc1, fc2 = st.columns(2)
    with fc1:
        st.write("##### 🌦 Weather Condition Impact on Demand Volume")
        weather_impact = filtered_master.groupby('weather_condition')['units_sold'].mean().reset_index()
        fig_weather = px.bar(weather_impact, x='weather_condition', y='units_sold', color='units_sold', color_continuous_scale='Oranges')
        st.plotly_chart(fig_weather, use_container_width=True)
    with fc2:
        st.write("##### 🏷 Average Discount Level Rate by Seasonal Windows")
        season_discount = filtered_master.groupby('season')['discount'].mean().reset_index()
        fig_season = px.line(season_discount, x='season', y='discount', markers=True, color_discrete_sequence=['#20c997'])
        st.plotly_chart(fig_season, use_container_width=True)
        
    st.markdown("---")
    st.write("##### 📦 Competitive Price Elasticity Vector Scatter View")
    sample_size = min(300, len(filtered_master))
    scatter_sample = filtered_master.sample(sample_size, random_state=42)
    fig_scatter = px.scatter(scatter_sample, x='unit_price', y='competitor_pricing', color='category', size='units_sold', title='Retail Pricing vs Competitor Limits')
    st.plotly_chart(fig_scatter, use_container_width=True)

def render_executive_summary_tab(filtered_triage):
    st.markdown("#### 📝 Phase 8: Financial Audit & Executive Report Summary")
    st.markdown("---")
    
    reorder_count = len(filtered_triage[filtered_triage['recommended_action'] == "Reorder Now"])
    total_locked_capital = filtered_triage['capital_tied_up'].sum()
    total_exposure = filtered_triage['rupee_impact_at_stake'].sum()
    
    st.markdown(f"""
    ### 📊 Project FORESIGHT Final Evaluation Memo
    
    **To**: Zidio Development Review Committee & NorthBay Living Operations Executive Board  
    **From**: Enterprise Data Science Implementation Lead  
    **Project Lifecycle Status**: Deployed Production Infrastructure Complete  
    
    ---
    
    #### 📋 1. Core Corporate Insights & Audit Findings
    *   **Total Monitored Ledger Scale**: Analyzed and verified **{len(filtered_triage):,} active core items** across tracking networks.
    *   **Active Pipeline Shortfalls**: Detected exactly **{reorder_count} critical product alerts** violating minimum safety reorder thresholds.
    *   **Warehouse Capital Footprint**: NorthBay Living currently maintains **₹{total_locked_capital:,.2f}** locked inside sitting inventory assets.
    *   Quantified Risk Liability Exposure: Mathematical modeling exposes a total network liability of ₹{total_exposure:,.2f} due to supply chain blockages.
    #### ⚙️ 2. Advanced Technical Implementation Lifecycle
    *   Phase 1-2 (ETL Infrastructure): Automated data clean pipelines tracking international date strings with mixed parsing parameters safely.
    *   Phase 3-4 (Feature Engineering): Synthesized local history lags and 7-day rolling standard deviations to capture localized velocity channels.
    *   Phase 5-6 (Predictive Forecasting Core): Trained a Location-Aware Random Forest Regressor to minimize prediction errors against naive historical benchmarks.
    *   Phase 7-8 (Productization & Deployment): Deployed a robust, responsive multi-tab control center web application supporting purchase ledger automated downloads.
    #### 🛡️ 3. Strategic Optimization Guidelines
    # 1.  Immediate Procurement Reordering: Execute the downloadable Excel purchase order spreadsheet to restock the {reorder_count} stockout items.
    # 2.  Liquidation Clearance Strategy: Run the Markdown Clearance Optimizer on Tab 1 to release locked capital from dead-stock items.
    # 3.  Model Monitoring Schedules: Schedule monthly pipeline script updates to preserve accuracy across season switches.""", unsafe_allow_html=True)