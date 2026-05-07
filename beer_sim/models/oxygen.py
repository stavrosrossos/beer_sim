"""Oxygen mass-transfer equations."""


def oxygen_transfer_rate(k_la: float, saturated_oxygen: float, dissolved_oxygen: float) -> float:
    """Return OTR = k_la * (C_star - C)."""

    return k_la * (saturated_oxygen - dissolved_oxygen)


def oxygen_consumption_rate(
    specific_oxygen_consumption_rate: float,
    biomass_g_m3: float,
    dissolved_oxygen: float,
    half_saturation: float,
) -> float:
    """Return yeast oxygen uptake in kg O2 m^-3 s^-1."""

    if half_saturation <= 0.0:
        raise ValueError("half_saturation must be positive")
    oxygen_factor = max(dissolved_oxygen, 0.0) / (half_saturation + max(dissolved_oxygen, 0.0))
    return specific_oxygen_consumption_rate * max(biomass_g_m3, 0.0) * oxygen_factor


def aerated_power(
    coefficient: float,
    ungassed_power: float,
    agitation_rate: float,
    impeller_diameter: float,
    gas_flow_rate: float,
) -> float:
    """Return the empirical aerated power input term from the spec."""

    if gas_flow_rate <= 0.0:
        raise ValueError("gas_flow_rate must be positive")
    term = (ungassed_power * agitation_rate * impeller_diameter**3) / gas_flow_rate**0.56
    return coefficient * term**-0.45
