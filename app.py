import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from model import run_model
from utils import plot_catalyst_deactivation, plot_pareto_front

st.set_page_config(
    page_title="SRR Refinery Digital Twin",
    page_icon="🏭",
    layout="wide"
)

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
st.caption("Simulation model only. No live refinery historian or plant data connected.")
