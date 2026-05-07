"""Microbial growth and cell-population equations."""

from __future__ import annotations

import math


def monod_specific_growth_rate(mu_max: float, substrate: float, ks: float) -> float:
    """Return mu = mu_max * S / (Ks + S)."""

    if substrate <= 0.0:
        return 0.0
    if ks < 0.0:
        raise ValueError("ks must be non-negative")
    return mu_max * substrate / (ks + substrate)


def viable_cells(total_cells: float, dead_cells: float) -> float:
    """Return viable cell concentration."""

    return max(total_cells - dead_cells, 0.0)


def cardinal_temperature_factor(
    temperature_c: float,
    minimum_c: float,
    optimum_c: float,
    maximum_c: float,
) -> float:
    """Return CTMI growth activity normalized to 1.0 at the optimum temperature."""

    if temperature_c <= minimum_c or temperature_c >= maximum_c:
        return 0.0

    numerator = (temperature_c - maximum_c) * (temperature_c - minimum_c) ** 2
    denominator = (optimum_c - minimum_c) * (
        (optimum_c - minimum_c) * (temperature_c - optimum_c)
        - (optimum_c - maximum_c) * (optimum_c + minimum_c - 2.0 * temperature_c)
    )
    if math.isclose(denominator, 0.0):
        return 0.0
    return max(numerator / denominator, 0.0)


def ethanol_inhibition_factor(ethanol_abv: float, tolerance_abv: float) -> float:
    """Return a smooth inhibition factor as ethanol approaches strain tolerance."""

    if tolerance_abv <= 0.0:
        raise ValueError("tolerance_abv must be positive")
    return max(1.0 - (ethanol_abv / tolerance_abv) ** 2, 0.0)


def lag_activity_factor(time: float, lag_time: float) -> float:
    """Return a gradual activity ramp after pitching."""

    if lag_time <= 0.0:
        return 1.0
    return 1.0 - math.exp(-time / lag_time)


def stress_adjusted_death_rate(
    base_death_rate: float,
    temperature_c: float,
    optimum_c: float,
    maximum_c: float,
    ethanol_abv: float,
    tolerance_abv: float,
) -> float:
    """Increase death rate under high-temperature and high-ethanol stress."""

    if base_death_rate < 0.0:
        raise ValueError("base_death_rate must be non-negative")

    temperature_span = max(maximum_c - optimum_c, 1.0)
    temperature_stress = max((temperature_c - optimum_c) / temperature_span, 0.0)
    ethanol_stress = max((ethanol_abv - 0.8 * tolerance_abv) / max(0.2 * tolerance_abv, 1.0e-9), 0.0)
    return base_death_rate * (1.0 + 6.0 * temperature_stress**2 + 4.0 * ethanol_stress**2)


def fopdt_target_population(time: float, lag_time: float, max_total_cells: float) -> float:
    """Return the delayed target population term for FOPDT growth models."""

    if time <= lag_time:
        return 0.0
    return max_total_cells
