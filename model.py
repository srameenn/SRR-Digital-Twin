import numpy as np

def run_model(days, wait, h2hc, feed):

    # ---------------- Catalyst Deactivation ----------------
    deactivation = np.exp(-0.003 * days)

    # ---------------- RON Model ----------------
    ron = (
        0.18 * wait +
        0.4 * feed -
        2.5 * h2hc
    ) * deactivation

    # ---------------- Yield Model ----------------
    yield_c5 = (
        100 -
        0.04 * wait +
        0.1 * feed -
        1.2 * h2hc
    ) * deactivation

    # ---------------- Coke Risk Model ----------------
    coke = (
        0.02 * wait -
        0.1 * h2hc +
        0.03 * days
    )

    coke = max(0, min(coke, 1))  # normalize 0–1

    return ron, yield_c5, coke