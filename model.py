import numpy as np

def run_model(days, naphthenes, aromatics):

    # Temperature increases slightly with catalyst aging
    temperature = 485 + 0.03 * days

    # Hydrogen to hydrocarbon ratio
    h2_hc = 4.5 - 0.0015 * days + 0.002 * (naphthenes - 30)

    # Predicted RON
    ron = (
        88
        + 0.18 * (temperature - 485)
        + 0.12 * (naphthenes - 30)
        + 0.20 * (aromatics - 10)
        - 0.015 * days
    )

    # Predicted C5+ yield
    yield_c5 = (
        92
        - 0.06 * (temperature - 485)
        + 0.05 * (naphthenes - 30)
        - 0.03 * (aromatics - 10)
    )

    # Coke formation risk
    coke = max(
        0,
        0.12
        + 0.0009 * (temperature - 485) ** 2
        + 0.0015 * days
        - 0.01 * h2_hc
    )

    return {
        "temperature": temperature,
        "h2_hc": h2_hc,
        "ron": ron,
        "yield": yield_c5,
        "coke": coke
    }
