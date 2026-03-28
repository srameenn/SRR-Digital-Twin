import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from model import run_model
from utils import plot_catalyst_deactivation, plot_pareto_front

st.set_page_config(
    page_title="SRR Refinery Digital Twin",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------- Custom Industrial Theme -----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #08111f 0%, #0f1c2e 100%);
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1500px;
}

[data-testid="stSidebar"] {
    background: #0b1624;
    border-right: 1px solid #1d324d;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    color: #e8f1ff;
    margin-bottom: 0;
}

.dashboard-subtitle {
    color: #8ea7c2;
    font-size: 16px;
    margin-top: -10px;
    margin-bottom: 20px;
}

.card {
    background: rgba(18, 32, 51, 0.95);
    border: 1px solid #243b57;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 0 18px rgba(0,0,0,0.25);
}

.metric-card {
    background: linear-gradient(145deg, #132238, #0d1727);
    border: 1px solid #29435f;
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0,0,0,0.25);
}

.metric-label {
    color: #7f96af;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: #f2f7ff;
    font-size: 34px;
    font-weight: 700;
}

.metric-unit {
    color: #4fd1c5;
    font-size: 15px;
}

.section-title {
    color: #dbe8ff;
    font-size: 24px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ----------- Header -----------
st.markdown('<div class="dashboard-title">🏭 SRR Refinery Digital Twin</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-subtitle">Advanced Catalytic Reforming Control Room | Physics-Informed Optimization Platform</div>', unsafe_allow_html=True)

# ----------- Sidebar Inputs -----------
st.sidebar.title("Plant Inputs")

stream_days = st.sidebar.slider("Catalyst Age (Days on Stream)", 0, 400, 180)
naphthenes = st.sidebar.slider("Feed Naphthenes (%)", 10, 40, 30)
aromatics = st.sidebar.slider("Feed Aromatics (%)", 5, 20, 12)

results = run_model(stream_days, naphthenes, aromatics)

# ----------- KPI Cards -----------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">Reactor Temp</div>
        <div class="metric-value">{results["temperature"]:.1f}</div>
        <div class="metric-unit">°C</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">H₂/HC Ratio</div>
        <div class="metric-value">{results["h2_hc"]:.2f}</div>
        <div class="metric-unit">mol/mol</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">RON</div>
        <div class="metric-value">{results["ron"]:.1f}</div>
        <div class="metric-unit">Research Octane</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">C5+ Yield</div>
        <div class="metric-value">{results["yield"]:.1f}</div>
        <div class="metric-unit">wt%</div>
    </div>
    ''', unsafe_allow_html=True)

with col5:
    coke_color = "#4ade80" if results["coke"] < 0.3 else "#f59e0b"
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">Coke Risk</div>
        <div class="metric-value" style="color:{coke_color}">{results["coke"]:.2f}</div>
        <div class="metric-unit">Index</div>
    </div>
    ''', unsafe_allow_html=True)

# ----------- Multi-variable Performance Graph -----------
st.markdown('<div class="section-title">Performance Trade-Off Analysis</div>', unsafe_allow_html=True)

x = np.linspace(470, 530, 50)
ron = 82 + 0.12 * (x - 470) + 0.03 * naphthenes
yield_curve = 97 - 0.08 * (x - 470)
coke = 0.15 + 0.0008 * (x - 470) ** 2

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(
    x=x, y=ron, mode="lines", name="RON",
    line=dict(color="#38bdf8", width=4)
))

fig.add_trace(go.Scatter(
    x=x, y=yield_curve, mode="lines", name="C5+ Yield",
    line=dict(color="#22c55e", width=4)
))

fig.add_trace(go.Scatter(
    x=x, y=coke, mode="lines", name="Coke Index",
    line=dict(color="#f97316", width=4, dash="dot")
), secondary_y=True)

fig.update_layout(
    height=450,
    paper_bgcolor="#111c2c",
    plot_bgcolor="#111c2c",
    font=dict(color="#dce7f5"),
    legend=dict(orientation="h", y=1.1),
    margin=dict(l=20, r=20, t=30, b=20)
)

fig.update_xaxes(title="Reactor Temperature (°C)", gridcolor="#20354d")
fig.update_yaxes(title="RON / Yield", gridcolor="#20354d")
fig.update_yaxes(title="Coke Risk", secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

# ----------- Bottom Charts -----------
left, right = st.columns(2)

with left:
    st.markdown('<div class="section-title">Catalyst Life Curve</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_catalyst_deactivation(), use_container_width=True)

with right:
    st.markdown('<div class="section-title">Pareto Optimization Front</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_pareto_front(), use_container_width=True)

st.caption("Simulation environment for catalytic reforming optimization. Not connected to real plant historian data.")
