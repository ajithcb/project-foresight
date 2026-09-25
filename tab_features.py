import streamlit as st
import pandas as pd
import plotly.express as px

def render_market_features_tab(filtered_master):
    st.markdown("#### 🌦 External Features & Predictive Model Dynamics")
    st.markdown("---")
    
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
