"""Simulation orchestration for beer process models."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp

from beer_sim.config import ETHANOL_DENSITY_KG_M3, SECONDS_PER_HOUR, SimulationConfig
from beer_sim.models.fermentation import ethanol_formation_rate, sugar_consumption_rate
from beer_sim.models.growth import (
    cardinal_temperature_factor,
    ethanol_inhibition_factor,
    lag_activity_factor,
    monod_specific_growth_rate,
    stress_adjusted_death_rate,
)
from beer_sim.models.oxygen import oxygen_consumption_rate, oxygen_transfer_rate
from beer_sim.models.quality import flavor_degradation_rate
from beer_sim.state import BrewState, default_initial_state


@dataclass(frozen=True)
class SimulationSummary:
    """Human-facing endpoint metrics."""

    final_abv: float
    residual_sugar: float
    attenuation: float
    final_viable_cells: float
    final_viability: float
    final_dissolved_oxygen_mg_l: float
    flavor_retention: float
    completion_time_hours: float | None
    risk_flags: tuple[str, ...]


@dataclass(frozen=True)
class SimulationResult:
    """Time series returned by the simulator."""

    time: NDArray[np.float64]
    states: list[BrewState]
    config: SimulationConfig
    initial_state: BrewState

    @property
    def summary(self) -> SimulationSummary:
        return summarize(self)


def rhs(time: float, values: NDArray[np.float64], config: SimulationConfig) -> NDArray[np.float64]:
    """Compute process derivatives for solve_ivp."""

    state = BrewState.from_vector(values)
    viable_cells = state.viable_cells
    strain = config.yeast.strain
    temperature_c = state.temperature - 273.15
    abv = ethanol_abv(state.ethanol)

    substrate_factor = monod_specific_growth_rate(
        mu_max=1.0,
        substrate=state.substrate,
        ks=config.yeast.ks,
    )
    temperature_factor = cardinal_temperature_factor(
        temperature_c,
        strain.temperature_min_c,
        strain.temperature_opt_c,
        strain.temperature_max_c,
    )
    ethanol_factor = ethanol_inhibition_factor(abv, config.yeast.ethanol_tolerance_abv)
    lag_factor = lag_activity_factor(time, config.yeast.lag_time)
    carrying_capacity_factor = max(1.0 - state.total_cells / config.yeast.max_total_cells, 0.0)

    mu = config.yeast.mu_opt * substrate_factor * temperature_factor * ethanol_factor * lag_factor
    death_rate = stress_adjusted_death_rate(
        config.yeast.base_death_rate,
        temperature_c,
        strain.temperature_opt_c,
        strain.temperature_max_c,
        abv,
        config.yeast.ethanol_tolerance_abv,
    )

    biomass_kg_m3 = viable_cells * config.yeast.biomass_per_cell
    biomass_g_m3 = biomass_kg_m3 * 1000.0

    d_total_cells = mu * viable_cells * carrying_capacity_factor
    d_dead_cells = death_rate * viable_cells
    d_substrate = (
        sugar_consumption_rate(
            config.yeast.sugar_uptake_rate,
            biomass_kg_m3,
            substrate_factor,
            temperature_factor,
            ethanol_factor,
        )
        if state.substrate > 0.0
        else 0.0
    )
    d_ethanol = ethanol_formation_rate(config.yeast.ethanol_yield, d_substrate)
    d_oxygen = oxygen_transfer_rate(
        config.oxygen.k_la,
        config.oxygen.saturation_concentration,
        state.dissolved_oxygen,
    ) - oxygen_consumption_rate(
        config.oxygen.specific_oxygen_consumption_rate,
        biomass_g_m3,
        state.dissolved_oxygen,
        config.oxygen.oxygen_half_saturation,
    )
    flavor_rate = config.quality.flavor_degradation_rate * config.quality.flavor_q10 ** (
        (temperature_c - 20.0) / 10.0
    )
    d_flavor = flavor_degradation_rate(concentration=state.flavor_compound, rate_constant=flavor_rate)
    d_temperature = 0.0

    return np.array(
        [
            d_substrate,
            d_total_cells,
            d_dead_cells,
            d_ethanol,
            d_oxygen,
            d_flavor,
            d_temperature,
        ],
        dtype=float,
    )


def simulate(
    config: SimulationConfig | None = None,
    initial_state: BrewState | None = None,
) -> SimulationResult:
    """Run a batch fermentation simulation."""

    config = config or SimulationConfig()
    initial_state = initial_state or default_initial_state()
    sample_count = int(config.duration / config.sample_interval) + 1
    sample_times = np.linspace(0.0, config.duration, sample_count)

    solution = solve_ivp(
        fun=lambda time, values: rhs(time, values, config),
        t_span=(0.0, config.duration),
        y0=initial_state.as_vector(),
        t_eval=sample_times,
        method="RK45",
        rtol=1.0e-6,
        atol=1.0e-9,
    )

    if not solution.success:
        raise RuntimeError(f"Simulation failed: {solution.message}")

    states = [BrewState.from_vector(solution.y[:, index]) for index in range(solution.y.shape[1])]
    return SimulationResult(time=solution.t, states=states, config=config, initial_state=initial_state)


def ethanol_abv(ethanol_concentration: float) -> float:
    """Convert ethanol kg/m^3 to approximate ABV percent."""

    return max(ethanol_concentration, 0.0) / ETHANOL_DENSITY_KG_M3 * 100.0


def apparent_attenuation(initial_sugar: float, residual_sugar: float) -> float:
    """Return the fraction of initial sugar consumed."""

    if initial_sugar <= 0.0:
        return 0.0
    return max(min((initial_sugar - residual_sugar) / initial_sugar, 1.0), 0.0)


def summarize(result: SimulationResult) -> SimulationSummary:
    """Compute endpoint metrics and process risk flags."""

    final = result.states[-1]
    initial = result.initial_state
    attenuation = apparent_attenuation(initial.substrate, final.substrate)
    viability = final.viable_cells / final.total_cells if final.total_cells > 0.0 else 0.0
    flavor_retention = final.flavor_compound / initial.flavor_compound if initial.flavor_compound > 0.0 else 0.0

    return SimulationSummary(
        final_abv=ethanol_abv(final.ethanol),
        residual_sugar=final.substrate,
        attenuation=attenuation,
        final_viable_cells=final.viable_cells,
        final_viability=viability,
        final_dissolved_oxygen_mg_l=final.dissolved_oxygen * 1000.0,
        flavor_retention=flavor_retention,
        completion_time_hours=_completion_time_hours(result),
        risk_flags=tuple(_risk_flags(result, attenuation, viability)),
    )


def _completion_time_hours(result: SimulationResult) -> float | None:
    initial_sugar = result.initial_state.substrate
    target_sugar = initial_sugar * 0.25
    for time, state in zip(result.time, result.states, strict=True):
        if state.substrate <= target_sugar:
            return float(time / SECONDS_PER_HOUR)
    return None


def _risk_flags(result: SimulationResult, attenuation: float, viability: float) -> list[str]:
    config = result.config
    initial = result.initial_state
    final = result.states[-1]
    strain = config.yeast.strain
    temperature_c = config.vessel.temperature - 273.15
    final_abv = ethanol_abv(final.ethanol)
    flags: list[str] = []

    if initial.total_cells < 6.0e12:
        flags.append("Low pitch rate may extend lag phase or increase stuck-fermentation risk.")
    if initial.dissolved_oxygen < 7.0e-3:
        flags.append("Initial dissolved oxygen is below the common 7-12 mg/L brewing target.")
    if temperature_c < strain.recommended_min_c or temperature_c > strain.recommended_max_c:
        flags.append("Fermentation temperature is outside the selected strain's normal operating range.")
    if final_abv > 0.85 * config.yeast.ethanol_tolerance_abv:
        flags.append("Predicted ethanol is near the selected strain's tolerance limit.")
    if attenuation < 0.65:
        flags.append("Low apparent attenuation suggests high residual sugar or slow fermentation.")
    if viability < 0.50:
        flags.append("Final yeast viability is low in this scenario.")
    if not flags:
        flags.append("No major process warnings from the current simplified model.")
    return flags
