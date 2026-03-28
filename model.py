import numpy as np

def run_model(days_on_stream, naphthenes, aromatics_feed):
    # Catalyst activity decreases with age
    catalyst_activity = max(0.68, 1.0 - 0.0008 * days_on_stream)

    # Recommended operating conditions
    temperature = 490 + 0.05 * days_on_stream
    temperature = np.clip(temperature, 490, 525)

    pressure = 18 - 0.012 * days_on_stream
    pressure = np.clip(pressure, 12, 18)

    h2_hc = 4.0 + 0.004 * days_on_stream
    h2_hc = np.clip(h2_hc, 4.0, 5.5)

    # Reformate RON model
    ron = (
        84
        + 0.24 * (temperature - 490)
        - 0.50 * (pressure - 15)
        - 0.70 * (h2_hc - 4)
        + 0.40 * (naphthenes - 25)
        + 0.32 * (aromatics_feed - 10)
        + 13 * (catalyst_activity - 0.8)
    )
    ron = np.clip(ron, 84, 102)

    # C5+ liquid yield model
    c5_yield = (
        92
        - 0.11 * (temperature - 490)
        + 0.22 * (pressure - 15)
        - 0.22 * (h2_hc - 4)
        + 0.08 * (naphthenes - 25)
        - 4.5 * (1 - catalyst_activity)
    )
    c5_yield = np.clip(c5_yield, 82, 96)

    # Coke tendency model
    coke = (
        0.12
        + 0.016 * (temperature - 490)
        - 0.045 * (h2_hc - 4)
        - 0.010 * (pressure - 15)
        + 0.0018 * days_on_stream
        + 0.002 * max(0, naphthenes - 30)
    )
    coke = np.clip(coke, 0.05, 1.0)

    # Hydrogen generation
    hydrogen = (
        120
        + 1.8 * (temperature - 490)
        + 0.9 * (naphthenes - 25)
        + 1.4 * (aromatics_feed - 10)
    )

    # Overall performance score
    score = 0.55 * ron + 0.30 * c5_yield - 10 * coke

    return {
        "temperature": round(float(temperature), 1),
        "pressure": round(float(pressure), 1),
        "h2_hc": round(float(h2_hc), 2),
        "ron": round(float(ron), 2),
        "yield": round(float(c5_yield), 2),
        "coke": round(float(coke), 2),
        "hydrogen": round(float(hydrogen), 1),
        "activity": round(float(catalyst_activity), 3),
        "score": round(float(score), 2)
    }
