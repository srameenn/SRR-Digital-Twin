import streamlit as st
import numpy as np
import plotly.graph_objects as go

from model import run_model
from utils import plot_catalyst_deactivation, plot_pareto_front

st.set_page_config(page_title="SRR Digital Twin", layout="wide")

st.title("🏭 SRR DIGITAL TWIN - CONTROL ROOM")

# ---------------- INPUT PANEL ----------------
st.sidebar.header("⚙️ Operating Inputs")

days = st.sidebar.slider("Days on Stream", 0, 400, 150)
wait = st.sidebar.slider("WAIT Temperature (°C)", 485, 525, 500)
h2hc = st.sidebar.slider("H2/HC Ratio", 2.5, 5.0, 3.2)
naph = st.sidebar.number_input("Naphthenes %", 10.0, 40.0, 25.0)
arom = st.sidebar.number_input("Aromatics %", 5.0, 25.0, 12.0)

feed = naph + 3.5 * arom

# ---------------- MODEL RUN ----------------
ron, yield_c5, coke = run_model(days, wait, h2hc, feed)

# ---------------- OUTPUT DASHBOARD ----------------
col1, col2, col3 = st.columns(3)

col1.metric("🔥 RON", f"{ron:.2f}")
col2.metric("🛢️ C5+ Yield", f"{yield_c5:.2f}%")
col3.metric("⚠️ Coke Index", f"{coke:.2f}")

st.markdown("---")

# ---------------- PLOTS ----------------
st.subheader("📈 Catalyst Deactivation Curve")
fig1 = plot_catalyst_deactivation()
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🎯 Pareto Optimization (RON vs Yield)")
fig2 = plot_pareto_front()
st.plotly_chart(fig2, use_container_width=True)

# ---------------- WARNING SYSTEM ----------------
if coke > 0.7:
    st.error("🚨 HIGH COKE RISK - Reduce severity immediately!")

if ron < 90:
    st.warning("⚠️ RON below target specification!")