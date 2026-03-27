import numpy as np
import plotly.graph_objects as go


# ---------------- Catalyst Life Curve ----------------
def plot_catalyst_deactivation():

    days = np.linspace(0, 400, 100)
    activity = np.exp(-0.003 * days)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=activity, mode='lines'))

    fig.update_layout(
        title="Catalyst Activity vs Days on Stream",
        xaxis_title="Days",
        yaxis_title="Activity"
    )

    return fig


# ---------------- Pareto Front ----------------
def plot_pareto_front():

    wait = np.linspace(485, 525, 30)
    h2hc = np.linspace(2.5, 5.0, 30)

    RON = []
    YIELD = []

    for w in wait:
        for h in h2hc:
            ron = 0.18*w + 0.4*60 - 2.5*h
            yld = 100 - 0.04*w + 0.1*60 - 1.2*h

            RON.append(ron)
            YIELD.append(yld)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=RON,
        y=YIELD,
        mode='markers',
        marker=dict(size=4)
    ))

    fig.update_layout(
        title="Pareto Front: RON vs Yield Trade-off",
        xaxis_title="RON",
        yaxis_title="C5+ Yield"
    )

    return fig