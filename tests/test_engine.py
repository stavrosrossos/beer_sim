import pytest

from beer_sim.config import SECONDS_PER_HOUR, SimulationConfig, VesselConfig
from beer_sim.engine import ethanol_abv, simulate
from beer_sim.state import make_initial_state


def test_default_simulation_produces_positive_abv_and_summary():
    result = simulate()

    assert result.summary.final_abv > 0.0
    assert result.summary.attenuation > 0.5
    assert result.summary.completion_time_hours is not None


def test_low_temperature_slows_fermentation():
    warm = simulate()
    cold_config = SimulationConfig(duration=7.0 * 24.0 * SECONDS_PER_HOUR)
    cold_initial = make_initial_state(temperature=278.15)
    cold_config = SimulationConfig(
        duration=cold_config.duration,
        sample_interval=cold_config.sample_interval,
        yeast=cold_config.yeast,
        oxygen=cold_config.oxygen,
        vessel=VesselConfig(temperature=278.15),
        quality=cold_config.quality,
    )
    cold = simulate(config=cold_config, initial_state=cold_initial)

    assert warm.summary.final_abv > cold.summary.final_abv


def test_ethanol_abv_conversion():
    assert ethanol_abv(78.9) == pytest.approx(10.0)
