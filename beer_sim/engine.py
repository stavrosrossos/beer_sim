"""Simulation orchestration for beer process models."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp

from beer_sim.config import ETHANOL_DENSITY_KG_M3, SECONDS_PER_HOUR, SimulationConfig
from beer_sim.models.growth import (
    cardinal_temperature_factor,
    lag_activity_factor,
    stress_adjusted_death_rate,
)
from beer_sim.models.oxygen import oxygen_consumption_rate, oxygen_transfer_rate
from beer_sim.models.quality import flavor_degradation_rate
from beer_sim.state import BrewState, default_initial_state


@dataclass(frozen=True)
class RateTerms:
    """Intermediate rate terms used by the ODE system."""

    mu: float
    q_ethanol: float
    biomass_growth: float
    ethanol_production: float
    substrate_consumption: float
    death_rate: float
    temperature_factor: float


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
    peak_vdk_mg_l: float
    final_vdk_mg_l: float
    final_acetaldehyde_mg_l: float
    final_esters_mg_l: float
    final_higher_alcohols_mg_l: float
    final_co2_g_l: float
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
    rates = primary_metabolism_rates(time, state, config)
    biomass_g_m3 = state.biomass * 1000.0

    d_total_cells = rates.biomass_growth / config.yeast.biomass_per_cell
    d_dead_cells = rates.death_rate * state.viable_cells
    d_biomass = rates.biomass_growth - rates.death_rate * state.biomass
    d_substrate = -rates.substrate_consumption if state.substrate > 0.0 else 0.0
    d_ethanol = rates.ethanol_production if state.substrate > 0.0 else 0.0
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

    flavor_temperature_factor = config.quality.flavor_q10 ** ((state.temperature - 293.15) / 10.0)
    d_vdk = (
        config.quality.vdk_yield * rates.biomass_growth
        - config.quality.vdk_reduction * flavor_temperature_factor * state.vdk * state.biomass
    )
    d_acetaldehyde = (
        config.quality.acetaldehyde_yield * rates.biomass_growth
        - config.quality.acetaldehyde_reduction
        * flavor_temperature_factor
        * state.acetaldehyde
        * state.biomass
    )
    d_esters = config.quality.ester_yield * rates.biomass_growth
    d_higher_alcohols = config.quality.higher_alcohol_yield * rates.biomass_growth
    d_co2 = config.quality.co2_yield * rates.substrate_consumption
    flavor_rate = config.quality.flavor_degradation_rate * flavor_temperature_factor
    d_flavor = flavor_degradation_rate(concentration=state.flavor_compound, rate_constant=flavor_rate)
    d_temperature = 0.0

    return np.array(
        [
            d_substrate,
            d_total_cells,
            d_dead_cells,
            d_biomass,
            d_ethanol,
            d_oxygen,
            d_flavor,
            d_vdk,
            d_acetaldehyde,
            d_esters,
            d_higher_alcohols,
            d_co2,
            d_temperature,
        ],
        dtype=float,
    )


def primary_metabolism_rates(time: float, state: BrewState, config: SimulationConfig) -> RateTerms:
    """Return Monod/Aiba biomass, ethanol, and substrate rates."""

    if state.substrate <= 0.0 or state.biomass <= 0.0:
        return RateTerms(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    substrate_factor_growth = state.substrate / (config.yeast.ks + state.substrate)
    substrate_factor_product = state.substrate / (config.yeast.product_ks + state.substrate)
    temperature_factor = _relative_temperature_factor(state.temperature - 273.15, config)
    lag_factor = lag_activity_factor(time, config.yeast.lag_time)
    growth_inhibition = math.exp(-config.yeast.ethanol_inhibition * state.ethanol)
    product_inhibition = math.exp(-config.yeast.product_inhibition * state.ethanol)

    mu = config.yeast.mu_opt * substrate_factor_growth * growth_inhibition * temperature_factor * lag_factor
    q_ethanol = (
        config.yeast.q_pmax
        * substrate_factor_product
        * product_inhibition
        * temperature_factor
        * lag_factor
    )
    biomass_growth = mu * state.biomass
    ethanol_production = q_ethanol * state.biomass
    substrate_consumption = (biomass_growth / config.yeast.biomass_yield) + (
        ethanol_production / config.yeast.ethanol_yield
    )
    temperature_c = state.temperature - 273.15
    death_rate = stress_adjusted_death_rate(
        config.yeast.base_death_rate,
        temperature_c,
        config.yeast.strain.temperature_opt_c,
        config.yeast.strain.temperature_max_c,
        ethanol_abv(state.ethanol),
        config.yeast.ethanol_tolerance_abv,
    )

    return RateTerms(
        mu=mu,
        q_ethanol=q_ethanol,
        biomass_growth=biomass_growth,
        ethanol_production=ethanol_production,
        substrate_consumption=substrate_consumption,
        death_rate=death_rate,
        temperature_factor=temperature_factor,
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
    peak_vdk = max(state.vdk for state in result.states) * 1000.0

    return SimulationSummary(
        final_abv=ethanol_abv(final.ethanol),
        residual_sugar=final.substrate,
        attenuation=attenuation,
        final_viable_cells=final.viable_cells,
        final_viability=viability,
        final_dissolved_oxygen_mg_l=final.dissolved_oxygen * 1000.0,
        flavor_retention=flavor_retention,
        peak_vdk_mg_l=peak_vdk,
        final_vdk_mg_l=final.vdk * 1000.0,
        final_acetaldehyde_mg_l=final.acetaldehyde * 1000.0,
        final_esters_mg_l=final.esters * 1000.0,
        final_higher_alcohols_mg_l=final.higher_alcohols * 1000.0,
        final_co2_g_l=final.co2,
        completion_time_hours=_completion_time_hours(result),
        risk_flags=tuple(_risk_flags(result, attenuation, viability)),
    )


def _relative_temperature_factor(temperature_c: float, config: SimulationConfig) -> float:
    strain = config.yeast.strain
    current = cardinal_temperature_factor(
        temperature_c,
        strain.temperature_min_c,
        strain.temperature_opt_c,
        strain.temperature_max_c,
    )
    reference = cardinal_temperature_factor(
        strain.reference_temperature_c,
        strain.temperature_min_c,
        strain.temperature_opt_c,
        strain.temperature_max_c,
    )
    if reference <= 0.0:
        return current
    return min(current / reference, 2.5)


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
    if final.vdk * 1000.0 > 0.10:
        flags.append("Final VDK/diacetyl proxy is above a common low sensory threshold.")
    if final.acetaldehyde * 1000.0 > 10.0:
        flags.append("Final acetaldehyde proxy is elevated; maturation may be incomplete.")
    if not flags:
        flags.append("No major process warnings from the current simplified model.")
    return flags
