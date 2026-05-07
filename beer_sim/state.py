"""State containers for the brewing simulation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class BrewState:
    """Concentrations and temperature using SI units."""

    substrate: float
    total_cells: float
    dead_cells: float
    ethanol: float
    dissolved_oxygen: float
    flavor_compound: float
    temperature: float

    def as_vector(self) -> NDArray[np.float64]:
        return np.array(
            [
                self.substrate,
                self.total_cells,
                self.dead_cells,
                self.ethanol,
                self.dissolved_oxygen,
                self.flavor_compound,
                self.temperature,
            ],
            dtype=float,
        )

    @classmethod
    def from_vector(cls, values: NDArray[np.float64]) -> "BrewState":
        return cls(
            substrate=max(float(values[0]), 0.0),
            total_cells=max(float(values[1]), 0.0),
            dead_cells=max(float(values[2]), 0.0),
            ethanol=max(float(values[3]), 0.0),
            dissolved_oxygen=max(float(values[4]), 0.0),
            flavor_compound=max(float(values[5]), 0.0),
            temperature=float(values[6]),
        )

    @property
    def viable_cells(self) -> float:
        return max(self.total_cells - self.dead_cells, 0.0)


def make_initial_state(
    substrate: float = 120.0,
    pitch_rate: float = 9.0e12,
    dissolved_oxygen: float = 8.0e-3,
    temperature: float = 293.15,
    flavor_compound: float = 1.0,
) -> BrewState:
    """Return a starting point using SI units."""

    return BrewState(
        substrate=substrate,
        total_cells=pitch_rate,
        dead_cells=0.0,
        ethanol=0.0,
        dissolved_oxygen=dissolved_oxygen,
        flavor_compound=flavor_compound,
        temperature=temperature,
    )


def default_initial_state() -> BrewState:
    """Return a representative 12 Plato ale starting point."""

    return make_initial_state()
