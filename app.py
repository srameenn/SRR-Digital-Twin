import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from model import run_model
from utils import plot_catalyst_deactivation, plot_pareto_front

# --- Page Setup ---
st.set_page_config(
    page_title="SRR Refinery Digital Twin",
    page_icon="🏭",
    layout="wide"
)

# --- CSS Styling ---
st.markdown("""
<style>
.main {
    background-color: #08111f;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1450px;
}

[data-testid="stSidebar"] {
    background-color: #0f1724;
}

.title {
    font-size: 42px;
    font-weight: 800;
    color: #e2e8f0;
}

.subtitle {
    font-size: 16px;
    color: #94a3b8;
    margin-bottom: 30px;
}

.metric-card {
    background: linear-gradient(145deg, #132238, #0b1725);
    border: 1px solid #22354a;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    box-shadow: 0px 0px 12px rgba(0,0,0,0.35);
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: white;
    font-size: 34px;
    font-weight: 700;
}

.metric-unit {
    color: #38bdf8;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# --- Title & Subtitle ---
st.markdown('<div class="title">🏭 SRR Refinery Digital Twin</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Advanced Catalytic Reforming Control Room | Physics-Informed Optimization Platform</div>', unsafe_allow_html=True)

# --- Sidebar Inputs ---
st.sidebar.header("Feed & Catalyst Inputs")
stream_days = st.sidebar.slider("Days on Stream", 0, 400, 120)
naphthenes = st.sidebar.slider("Feed Naphthenes (wt%)", 15, 45, 28)
aromatics = st.sidebar.slider("Feed Aromatics (wt%)", 5, 25, 10)

results = run_model(stream_days, naphthenes, aromatics)

# --- Helper for KPI Card ---
def kpi_card(label, value, unit):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>
    """, unsafe_allow_html=True)

# --- KPI Row 1 ---
col1, col2, col3, col4 = st.columns(4)
with col1: kpi_card("RON", results['ron'], "Research Octane")
with col2: kpi_card("C5+ Yield", results['yield'], "wt%")
with col3: kpi_card("Coke Index", results['coke'], "Relative Risk")
with col4: kpi_card("Hydrogen Production", results['hydrogen'], "Nm³/m³")

st.markdown("---")

# --- KPI Row 2 ---
col5, col6, col7, col8 = st.columns(4)
with col5: st.metric("Temperature", f"{results['temperature']} °C")
with col6: st.metric("Pressure", f"{results['pressure']} bar")
with col7: st.metric("H2/HC Ratio", f"{results['h2_hc']}")
with col8: st.metric("Catalyst Activity", f"{results['activity']}")

# --- Trade-off Chart ---
st.subheader("RON vs Yield vs Coke Trade-Off")
temps = np.linspace(490, 525, 40)
ron_curve = 88 + 0.22 * (temps - 490)
yield_curve = 94 - 0.12 * (temps - 490)
coke_curve = 0.1 + 0.018 * (temps - 490)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=temps, y=ron_curve, mode="lines", name="RON",
                         line=dict(color="#38bdf8", width=4)), secondary_y=False)
fig.add_trace(go.Scatter(x=temps, y=yield_curve, mode="lines", name="Yield",
                         line=dict(color="#22c55e", width=4)), secondary_y=False)
fig.add_trace(go.Scatter(x=temps, y=coke_curve, mode="lines", name="Coke",
                         line=dict(color="#f97316", width=4, dash="dot")), secondary_y=True)

fig.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827", font=dict(color="white"), height=500,
                  legend=dict(orientation="h"))
fig.update_xaxes(title="Reactor Temperature (°C)")
fig.update_yaxes(title="RON / Yield", secondary_y=False)
fig.update_yaxes(title="Coke Index", secondary_y=True)
st.plotly_chart(fig, use_container_width=True)

# --- Bottom Charts ---
col9, col10 = st.columns(2)
with col9: st.plotly_chart(plot_catalyst_deactivation(), use_container_width=True)
with col10: st.plotly_chart(plot_pareto_front(), use_container_width=True)

# --- Caption ---
st.caption("Simulation model only. No live refinery historian or plant data connected.")
