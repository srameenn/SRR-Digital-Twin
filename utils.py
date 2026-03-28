import numpy as np
import plotly.graph_objects as go

def plot_catalyst_deactivation():
    days = np.arange(0, 401)
    activity = np.maximum(0.68, 1.0 - 0.0008 * days)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days,
        y=activity,
        mode="lines",
        name="Catalyst Activity",
        line=dict(color="#38bdf8", width=4)
    ))

    fig.update_layout(
        title="Catalyst Life Curve",
        xaxis_title="Days on Stream",
        yaxis_title="Relative Catalyst Activity",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="white"),
        height=400
    )
    return fig

def plot_pareto_front():
    temperature = np.linspace(490, 525, 50)
    ron = 88 + 0.22 * (temperature - 490)
    yield_curve = 94 - 0.12 * (temperature - 490)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yield_curve,
        y=ron,
        mode="lines+markers",
        marker=dict(size=7, color="#22c55e"),
        line=dict(width=3, color="#22c55e"),
        name="Pareto Front"
    ))

    fig.update_layout(
        title="Pareto Front: Yield vs RON",
        xaxis_title="C5+ Yield (%)",
        yaxis_title="RON",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="white"),
        height=400
    )
    return fig
