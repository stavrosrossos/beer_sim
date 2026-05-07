"""Substrate consumption and ethanol formation equations."""


def sugar_consumption_rate(
    specific_substrate_rate: float,
    biomass: float,
    substrate_factor: float = 1.0,
    temperature_factor: float = 1.0,
    inhibition_factor: float = 1.0,
) -> float:
    """Return fermentable sugar depletion in kg m^-3 s^-1."""

    activity = max(substrate_factor, 0.0) * max(temperature_factor, 0.0) * max(inhibition_factor, 0.0)
    return -specific_substrate_rate * max(biomass, 0.0) * activity


def ethanol_formation_rate(yield_coefficient: float, sugar_depletion_rate: float) -> float:
    """Return dP/dt = Yps * (-dS/dt)."""

    return yield_coefficient * max(-sugar_depletion_rate, 0.0)


def ethanol_abv(ethanol_concentration: float, ethanol_density: float = 789.0) -> float:
    """Convert ethanol concentration in kg/m^3 to approximate ABV percent."""

    return max(ethanol_concentration, 0.0) / ethanol_density * 100.0
