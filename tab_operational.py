import streamlit as st
import pandas as pd
import plotly.express as px
import io

def render_operational_matrix_tab(filtered_triage):
    st.markdown("#### 🏬 Central Warehouse Triage Control Panel")
    st.markdown("---")
    
    # What-If Planning Scenario Simulators
    st.markdown("##### ⚙️ Simulation Modifiers: What-If Optimization Scenarios")
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        holding_cost_rate = st.slider("Annual Warehouse Holding Cost Rate (% of Product Cost):", min_value=5, max_value=40, value=18)
    with sim_col2:
        target_safety_days = st.slider("Target Safety Stock Cushion Runway (Days):", min_value=7, max_value=60, value=30)
        
    sim_triage = filtered_triage.copy()
    sim_triage['annual_holding_cost'] = sim_triage['capital_tied_up'] * (holding_cost_rate / 100)
    
    # Dead-stock Liquidations Markdown Optimizer
    st.markdown("---")
    st.markdown("##### 📉 Dead-Stock Markdown & Margin Clearance Optimizer")
    overstock_items = sim_triage[sim_triage['recommended_action'] == "Markdown / Clear"]
    if not overstock_items.empty:
        clearance_discount = st.slider("Simulate Clearance Discount Rate (%):", min_value=10, max_value=70, value=30)
        recovered_cash = overstock_items['capital_tied_up'].sum() * (1 - (clearance_discount / 100))
        margin_hit = overstock_items['capital_tied_up'].sum() * (clearance_discount / 100)
        
        md_c1, md_c2 = st.columns(2)
        md_c1.metric("Projected Working Capital Recovered", f"₹{recovered_cash:,.2f}")
        md_c2.metric("Projected Margin Liquidation Hit", f"₹{margin_hit:,.2f}", delta="- Margin Loss", delta_color="inverse")
    else:
        st.success("✅ Operational Excellence: Zero dead-stock overstock anomalies detected inside profiles.")

    # High-End Dark-Theme Plotly Charts Integration
    st.markdown("---")
    st.markdown("##### 📊 Interactive Risk Matrix Profiles")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        exposure_df = sim_triage.groupby('category')['rupee_impact_at_stake'].sum().reset_index()
        fig_exposure = px.bar(
            exposure_df, x='category', y='rupee_impact_at_stake',
            labels={'category': 'Product Category', 'rupee_impact_at_stake': 'Exposure Value (₹)'},
            template="plotly_dark"
        )
        fig_exposure.update_layout(
            title_text='Net Financial Liability Exposure By Category',
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af")
        )
        fig_exposure.update_traces(marker_color='#ef4444', marker_line_color='#b91c1c', marker_line_width=1)
        st.plotly_chart(fig_exposure, use_container_width=True)
        
    with chart_col2:
        action_mix = sim_triage['recommended_action'].value_counts().reset_index()
        action_mix.columns = ['Triage Status', 'Volume']
        
        # Hyper-Advanced Fix: Lock down distinct contrast colors per category value
        color_map = {
            "Reorder Now": "#ef4444",       # Vivid Alert Red
            "Markdown / Clear": "#f59e0b",   # Operational Warning Amber/Gold
            "Healthy": "#10b981",            # Stable Growth Green
            "Watch / Volatile": "#8b5cf6"    # Speculative Volatility Purple
        }
        
        fig_pie = px.pie(
            action_mix, values='Volume', names='Triage Status', 
            template="plotly_dark", hole=0.4,
            color='Triage Status',
            color_discrete_map=color_map
        )
        fig_pie.update_layout(
            title_text='Warehouse Strategy Allocation Mix',
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af")
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Automated Supplier PO spreadsheet pipe
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
    else:
        st.info("No immediate replenishment orders required for current item filters.")

    st.markdown("---")
    st.write("##### 🔍 Master Operational Inventory Fleet Ledger Workspace")
    st.dataframe(
        sim_triage[['sku_id', 'category', 'subcategory', 'total_on_hand', 'days_of_supply', 'capital_tied_up', 'recommended_action', 'rupee_impact_at_stake']],
        column_config={
            "sku_id": "SKU Code", "category": "Category", "subcategory": "Subcategory",
            "total_on_hand": "Physical Stock", "days_of_supply": "Runway (Days of Supply)", 
            "capital_tied_up": "Capital Tied-Up (₹)", "recommended_action": "Triage Action Group", 
            "rupee_impact_at_stake": st.column_config.NumberColumn("Exposure Risk (₹)", format="₹%.2f")
        },
        width="stretch", hide_index=True
    )

