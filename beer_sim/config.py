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
    q_pmax: float
    product_ks: float
    ethanol_inhibition: float
    product_inhibition: float
    biomass_yield: float
    biomass_per_cell: float
    temperature_min_c: float
    temperature_opt_c: float
    temperature_max_c: float
    recommended_min_c: float
    recommended_max_c: float

    @property
    def default_temperature_k(self) -> float:
        return ((self.recommended_min_c + self.recommended_max_c) / 2.0) + 273.15

    @property
    def reference_temperature_c(self) -> float:
        return (self.recommended_min_c + self.recommended_max_c) / 2.0


STRAIN_PRESETS: dict[str, StrainPreset] = {
    "w3470": StrainPreset(
        key="w3470",
        label="Literature lager W34/70",
        organism="Saccharomyces cerevisiae W34/70",
        mu_opt=0.0222 / SECONDS_PER_HOUR,
        ks=237.0,
        base_death_rate=0.005 / SECONDS_PER_HOUR,
        lag_time=8.0 * SECONDS_PER_HOUR,
        max_total_cells=1.2e14,
        ethanol_tolerance_abv=8.0,
        ethanol_yield=0.43,
        sugar_uptake_rate=1.0 / SECONDS_PER_HOUR,
        q_pmax=1.25 / SECONDS_PER_HOUR,
        product_ks=503.0,
        ethanol_inhibition=0.05,
        product_inhibition=0.02,
        biomass_yield=0.47,
        biomass_per_cell=2.0e-14,
        temperature_min_c=1.0,
        temperature_opt_c=22.0,
        temperature_max_c=36.0,
        recommended_min_c=13.0,
        recommended_max_c=17.0,
    ),
    "ale": StrainPreset(
        key="ale",
        label="Ale yeast",
        organism="Saccharomyces cerevisiae",
        mu_opt=0.30 / SECONDS_PER_HOUR,
        ks=35.0,
        base_death_rate=0.01 / SECONDS_PER_HOUR,
        lag_time=6.0 * SECONDS_PER_HOUR,
        max_total_cells=1.4e14,
        ethanol_tolerance_abv=10.0,
        ethanol_yield=0.48,
        sugar_uptake_rate=2.0 / SECONDS_PER_HOUR,
        q_pmax=1.40 / SECONDS_PER_HOUR,
        product_ks=120.0,
        ethanol_inhibition=0.08,
        product_inhibition=0.06,
        biomass_yield=0.20,
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
        ks=80.0,
        base_death_rate=0.008 / SECONDS_PER_HOUR,
        lag_time=9.0 * SECONDS_PER_HOUR,
        max_total_cells=1.2e14,
        ethanol_tolerance_abv=8.0,
        ethanol_yield=0.48,
        sugar_uptake_rate=1.2 / SECONDS_PER_HOUR,
        q_pmax=1.10 / SECONDS_PER_HOUR,
        product_ks=180.0,
        ethanol_inhibition=0.10,
        product_inhibition=0.08,
        biomass_yield=0.18,
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
        ks=40.0,
        base_death_rate=0.006 / SECONDS_PER_HOUR,
        lag_time=7.0 * SECONDS_PER_HOUR,
        max_total_cells=1.2e14,
        ethanol_tolerance_abv=7.0,
        ethanol_yield=0.46,
        sugar_uptake_rate=1.6 / SECONDS_PER_HOUR,
        q_pmax=1.00 / SECONDS_PER_HOUR,
        product_ks=150.0,
        ethanol_inhibition=0.11,
        product_inhibition=0.09,
        biomass_yield=0.18,
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

    strain: StrainPreset = field(default_factory=lambda: STRAIN_PRESETS["w3470"])
    mu_opt: float = STRAIN_PRESETS["w3470"].mu_opt
    ks: float = STRAIN_PRESETS["w3470"].ks
    base_death_rate: float = STRAIN_PRESETS["w3470"].base_death_rate
    lag_time: float = STRAIN_PRESETS["w3470"].lag_time
    max_total_cells: float = STRAIN_PRESETS["w3470"].max_total_cells
    ethanol_tolerance_abv: float = STRAIN_PRESETS["w3470"].ethanol_tolerance_abv
    ethanol_yield: float = STRAIN_PRESETS["w3470"].ethanol_yield
    sugar_uptake_rate: float = STRAIN_PRESETS["w3470"].sugar_uptake_rate
    q_pmax: float = STRAIN_PRESETS["w3470"].q_pmax
    product_ks: float = STRAIN_PRESETS["w3470"].product_ks
    ethanol_inhibition: float = STRAIN_PRESETS["w3470"].ethanol_inhibition
    product_inhibition: float = STRAIN_PRESETS["w3470"].product_inhibition
    biomass_yield: float = STRAIN_PRESETS["w3470"].biomass_yield
    biomass_per_cell: float = STRAIN_PRESETS["w3470"].biomass_per_cell

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
            q_pmax=preset.q_pmax,
            product_ks=preset.product_ks,
            ethanol_inhibition=preset.ethanol_inhibition,
            product_inhibition=preset.product_inhibition,
            biomass_yield=preset.biomass_yield,
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
    temperature: float = 288.15
    wall_area: float = 0.25
    wall_thickness: float = 0.002
    thermal_conductivity: float = 0.6


@dataclass(frozen=True)
class QualityConfig:
    """Flavor-metabolite model settings in SI-compatible units."""

    flavor_degradation_rate: float = 1.0e-8
    flavor_q10: float = 2.0
    vdk_yield: float = 6.5e-6
    vdk_reduction: float = 7.92e-9
    acetaldehyde_yield: float = 1.177e-4
    acetaldehyde_reduction: float = 3.78e-9
    ester_yield: float = 1.732e-4
    higher_alcohol_yield: float = 7.33e-5
    co2_yield: float = 0.489


@dataclass(frozen=True)
class SimulationConfig:
    """Top-level simulation settings."""

    duration: float = 7.0 * 24.0 * SECONDS_PER_HOUR
    sample_interval: float = 1.0 * SECONDS_PER_HOUR
    yeast: YeastKinetics = field(default_factory=YeastKinetics)
    oxygen: OxygenTransferConfig = field(default_factory=OxygenTransferConfig)
    vessel: VesselConfig = field(default_factory=VesselConfig)
    quality: QualityConfig = field(default_factory=QualityConfig)
