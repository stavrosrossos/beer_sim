"""Heat transfer and temperature-dependent kinetics."""

from __future__ import annotations

import math

from beer_sim.config import R_GAS


def arrhenius_rate(pre_exponential: float, activation_energy: float, temperature: float) -> float:
    """Return k = k0 * exp(-Ea / (R * T))."""

    if temperature <= 0.0:
        raise ValueError("temperature must be greater than absolute zero")
    return pre_exponential * math.exp(-activation_energy / (R_GAS * temperature))


def fourier_heat_transfer(
    thermal_conductivity: float,
    area: float,
    temperature_delta: float,
    wall_thickness: float,
) -> float:
    """Return q = K_a * A * delta_T / X."""

    if wall_thickness <= 0.0:
        raise ValueError("wall_thickness must be positive")
    return thermal_conductivity * area * temperature_delta / wall_thickness
