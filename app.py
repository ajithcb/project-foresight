import sys
import os

# Dynamic absolute path directory injection logic to protect local namespace lookups
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import streamlit as st
from dashboard_pipeline import get_filter_metadata, extract_and_filter_matrices
import tab_operational as t1
import tab_commercial as t2
import tab_features as t3
import tab_summary as t4

# Configure Enterprise Page Environment
st.set_page_config(page_title="FORESIGHT", page_icon="📈", layout="wide")

# Premium High-End Corporate Theme Injection
st.markdown("""
    <style>
    /* Global Background Adjustments */
    .stApp {
        background-color: #0d1117;
    }
    
    /* Professional Unified Metric Card containers */
    .metric-card-container {
        background: linear-gradient(145deg, #1f2937, #111827);
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #374151;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card-container:hover {
        transform: translateY(-2px);
    }
    .metric-card-lbl {
        font-size: 11px;
        color: #9ca3af;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    .metric-card-val {
        font-size: 32px;
        color: #f9fafb;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* Modernized Tab Layout overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #111827;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1f2937;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: pre-wrap;
        background-color: transparent;
        color: #9ca3af !important;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 14px;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

try:
    regions_list, categories_list = get_filter_metadata()
except Exception as e:
    st.error(f"❌ Critical Data Directory Pathway Missing: {e}")
    st.stop()

# --- THE WEST COMPONENT: GLOBAL INTERACTIVE CONTROL PANEL ---
st.sidebar.header("🎛 Control Filtering Console")
selected_regions = st.sidebar.multiselect("Geographic Regions:", options=regions_list, default=regions_list)
selected_categories = st.sidebar.multiselect("Product Category Domain:", options=categories_list, default=categories_list)

# Load data matrices from pipeline engine
filtered_master, filtered_triage = extract_and_filter_matrices(selected_regions, selected_categories)

if filtered_master is None or filtered_triage is None:
    st.error("❌ Dependencies uninitialized. Run forecast.py and risk.py to sync files.")
else:
    # Set the official application header
    st.title("📈FORESIGHT")
    st.caption(f"Enterprise Analytics Hub Portfolio — Evaluation Horizon Snapshot Date: `{filtered_triage['date'].max()}`")
    st.markdown("---")

    # --- THE NORTH COMPONENT: ADVANCED EXECUTIVE KPI BANNER ---
    reorder_skus = len(filtered_triage[filtered_triage['recommended_action'] == "Reorder Now"])
    total_capital_locked = filtered_triage['capital_tied_up'].sum()
    total_risk_exposure = filtered_triage['rupee_impact_at_stake'].sum()
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
            <div class="metric-card-container" style="border-top: 4px solid #3b82f6;">
                <div class="metric-card-lbl">Total Active SKUs</div>
                <div class="metric-card-val">{len(filtered_triage):,} items</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div class="metric-card-container" style="border-top: 4px solid #ef4444;">
                <div class="metric-card-lbl">Critical Reorder Alerts</div>
                <div class="metric-card-val">{reorder_skus} SKUs</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div class="metric-card-container" style="border-top: 4px solid #f59e0b;">
                <div class="metric-card-lbl">Total Capital Tied Up</div>
                <div class="metric-card-val">₹{total_capital_locked:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
            <div class="metric-box-container" class="metric-card-container" style="border-top: 4px solid #10b981;">
                <div class="metric-card-lbl">Active Financial Risk</div>
                <div class="metric-card-val">₹{total_risk_exposure:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)

    # --- THE EAST/CENTER COMPONENT: FOUR-TAB DATA VISUALIZATION MODULES ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Operational Risk Matrix", 
        "📈 Commercial Sales Intelligence", 
        "🌦 Market Features Analytics",
        "📝 Final Executive Summary"
    ])

    with tab1:
        t1.render_operational_matrix_tab(filtered_triage)
    with tab2:
        t2.render_commercial_sales_tab(filtered_master)
    with tab3:
        t3.render_market_features_tab(filtered_master)
    with tab4:
        t4.render_executive_summary_tab(filtered_triage, reorder_skus, total_capital_locked, total_risk_exposure)
