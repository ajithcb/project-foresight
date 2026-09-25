import streamlit as st
import pandas as pd
import plotly.express as px

def render_commercial_sales_tab(filtered_master):
    st.markdown("#### 📈 Enterprise Revenue & Velocity Performance Channels")
    st.markdown("---")
    
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
