"""Beer fermentation and brewing process simulation package."""

from beer_sim.config import SimulationConfig
from beer_sim.state import BrewState

__all__ = ["BrewState", "SimulationConfig", "SimulationResult", "simulate"]


def __getattr__(name: str):
    if name in {"SimulationResult", "simulate"}:
        from beer_sim.engine import SimulationResult, simulate

        return {"SimulationResult": SimulationResult, "simulate": simulate}[name]
    raise AttributeError(f"module 'beer_sim' has no attribute {name!r}")
