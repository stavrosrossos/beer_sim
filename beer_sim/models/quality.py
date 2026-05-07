"""Beer and wort quality degradation models."""


def flavor_degradation_rate(concentration: float, rate_constant: float, order: float = 1.0) -> float:
    """Return dCa/dt for -dCa/dt = k * Ca**n."""

    if concentration <= 0.0:
        return 0.0
    return -rate_constant * concentration**order
