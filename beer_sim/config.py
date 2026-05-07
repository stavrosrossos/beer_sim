"""Configuration defaults for SI-unit beer process simulations."""

from __future__ import annotations

from dataclasses import dataclass, field, replace


SECONDS_PER_HOUR = 3600.0
R_GAS = 8.314
ETHANOL_DENSITY_KG_M3 = 789.0


@dataclass(frozen=True)
class StrainPreset:
    """Scientifically meaningful yeast parameters in SI units."""

    key: str
    label: str
    organism: str
    mu_opt: float
    ks: float
    base_death_rate: float
    lag_time: float
    max_total_cells: float
    ethanol_tolerance_abv: float
    ethanol_yield: float
    sugar_uptake_rate: float
    biomass_per_cell: float
    temperature_min_c: float
    temperature_opt_c: float
    temperature_max_c: float
    recommended_min_c: float
    recommended_max_c: float

    @property
    def default_temperature_k(self) -> float:
        return ((self.recommended_min_c + self.recommended_max_c) / 2.0) + 273.15


STRAIN_PRESETS: dict[str, StrainPreset] = {
    "ale": StrainPreset(
        key="ale",
        label="Ale yeast",
        organism="Saccharomyces cerevisiae",
        mu_opt=0.30 / SECONDS_PER_HOUR,
        ks=1.0,
        base_death_rate=0.01 / SECONDS_PER_HOUR,
        lag_time=6.0 * SECONDS_PER_HOUR,
        max_total_cells=1.4e14,
        ethanol_tolerance_abv=10.0,
        ethanol_yield=0.48,
        sugar_uptake_rate=2.0 / SECONDS_PER_HOUR,
        biomass_per_cell=2.0e-14,
        temperature_min_c=3.0,
        temperature_opt_c=30.0,
        temperature_max_c=41.0,
        recommended_min_c=18.0,
        recommended_max_c=22.0,
    ),
    "lager": StrainPreset(
        key="lager",
        label="Lager yeast",
        organism="Saccharomyces pastorianus",
        mu_opt=0.18 / SECONDS_PER_HOUR,
        ks=1.0,
        base_death_rate=0.008 / SECONDS_PER_HOUR,
        lag_time=9.0 * SECONDS_PER_HOUR,
        max_total_cells=1.2e14,
        ethanol_tolerance_abv=8.0,
        ethanol_yield=0.48,
        sugar_uptake_rate=1.2 / SECONDS_PER_HOUR,
        biomass_per_cell=2.0e-14,
        temperature_min_c=1.0,
        temperature_opt_c=22.0,
        temperature_max_c=36.0,
        recommended_min_c=10.0,
        recommended_max_c=14.0,
    ),
    "probiotic": StrainPreset(
        key="probiotic",
        label="Probiotic yeast",
        organism="Saccharomyces boulardii",
        mu_opt=0.28 / SECONDS_PER_HOUR,
        ks=1.0,
        base_death_rate=0.006 / SECONDS_PER_HOUR,
        lag_time=7.0 * SECONDS_PER_HOUR,
        max_total_cells=1.2e14,
        ethanol_tolerance_abv=7.0,
        ethanol_yield=0.46,
        sugar_uptake_rate=1.6 / SECONDS_PER_HOUR,
        biomass_per_cell=2.0e-14,
        temperature_min_c=5.0,
        temperature_opt_c=37.0,
        temperature_max_c=42.0,
        recommended_min_c=30.0,
        recommended_max_c=37.0,
    ),
}


@dataclass(frozen=True)
class YeastKinetics:
    """Yeast kinetic parameters in SI units."""

    strain: StrainPreset = field(default_factory=lambda: STRAIN_PRESETS["ale"])
    mu_opt: float = STRAIN_PRESETS["ale"].mu_opt
    ks: float = STRAIN_PRESETS["ale"].ks
    base_death_rate: float = STRAIN_PRESETS["ale"].base_death_rate
    lag_time: float = STRAIN_PRESETS["ale"].lag_time
    max_total_cells: float = STRAIN_PRESETS["ale"].max_total_cells
    ethanol_tolerance_abv: float = STRAIN_PRESETS["ale"].ethanol_tolerance_abv
    ethanol_yield: float = STRAIN_PRESETS["ale"].ethanol_yield
    sugar_uptake_rate: float = STRAIN_PRESETS["ale"].sugar_uptake_rate
    biomass_per_cell: float = STRAIN_PRESETS["ale"].biomass_per_cell

    @classmethod
    def from_preset(cls, preset_key: str, mu_multiplier: float = 1.0) -> "YeastKinetics":
        preset = STRAIN_PRESETS[preset_key]
        return cls(
            strain=preset,
            mu_opt=preset.mu_opt * mu_multiplier,
            ks=preset.ks,
            base_death_rate=preset.base_death_rate,
            lag_time=preset.lag_time,
            max_total_cells=preset.max_total_cells,
            ethanol_tolerance_abv=preset.ethanol_tolerance_abv,
            ethanol_yield=preset.ethanol_yield,
            sugar_uptake_rate=preset.sugar_uptake_rate,
            biomass_per_cell=preset.biomass_per_cell,
        )

    def with_updates(self, **updates: float) -> "YeastKinetics":
        return replace(self, **updates)


@dataclass(frozen=True)
class OxygenTransferConfig:
    """Oxygen mass-transfer parameters in SI units."""

    k_la: float = 0.20 / SECONDS_PER_HOUR
    saturation_concentration: float = 10.0e-3
    specific_oxygen_consumption_rate: float = 8.53e-11
    oxygen_half_saturation: float = 0.5e-3


@dataclass(frozen=True)
class VesselConfig:
    """Simplified process vessel geometry and operating conditions."""

    volume: float = 0.02
    temperature: float = 293.15
    wall_area: float = 0.25
    wall_thickness: float = 0.002
    thermal_conductivity: float = 0.6


@dataclass(frozen=True)
class QualityConfig:
    """Simplified product quality model settings."""

    flavor_degradation_rate: float = 1.0e-8
    flavor_q10: float = 2.0


@dataclass(frozen=True)
class SimulationConfig:
    """Top-level simulation settings."""

    duration: float = 7.0 * 24.0 * SECONDS_PER_HOUR
    sample_interval: float = 1.0 * SECONDS_PER_HOUR
    yeast: YeastKinetics = field(default_factory=YeastKinetics)
    oxygen: OxygenTransferConfig = field(default_factory=OxygenTransferConfig)
    vessel: VesselConfig = field(default_factory=VesselConfig)
    quality: QualityConfig = field(default_factory=QualityConfig)
