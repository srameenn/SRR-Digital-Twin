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
st.caption("Simulation environment for catalytic reforming optimization. Not connected to real plant historian data.")
