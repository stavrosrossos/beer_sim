"""Lautering flow model."""

from __future__ import annotations

import math


def darcy_filtered_volume(
    pressure_delta: float,
    pore_radius: float,
    time: float,
    porosity_factor: float,
    bed_factor: float,
    viscosity: float,
    bed_length: float,
) -> float:
    """Return filtered volume from the Darcy-law form in the spec."""

    if viscosity <= 0.0:
        raise ValueError("viscosity must be positive")
    if bed_length <= 0.0:
        raise ValueError("bed_length must be positive")
    numerator = math.pi * pressure_delta * pore_radius**4 * time * porosity_factor * bed_factor
    return numerator / (8.0 * viscosity * bed_length)
