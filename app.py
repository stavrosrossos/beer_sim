"""Interactive Streamlit MVP for fermentation process sensitivity."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from beer_sim.config import (
    SECONDS_PER_HOUR,
    STRAIN_PRESETS,
    OxygenTransferConfig,
    QualityConfig,
    SimulationConfig,
    VesselConfig,
    YeastKinetics,
)
from beer_sim.engine import ethanol_abv, simulate
from beer_sim.state import make_initial_state


def make_dataframe(result) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Time (h)": result.time / SECONDS_PER_HOUR,
            "Sugar (g/L)": [state.substrate for state in result.states],
            "Ethanol (g/L)": [state.ethanol for state in result.states],
            "ABV (%)": [ethanol_abv(state.ethanol) for state in result.states],
            "Viable yeast (million cells/mL)": [state.viable_cells / 1.0e12 for state in result.states],
            "Dead yeast (million cells/mL)": [state.dead_cells / 1.0e12 for state in result.states],
            "Dissolved oxygen (mg/L)": [state.dissolved_oxygen * 1000.0 for state in result.states],
            "Flavor retention (%)": [state.flavor_compound * 100.0 for state in result.states],
        }
    )


st.set_page_config(page_title="Beer Fermentation Simulator", layout="wide")
st.title("Beer Fermentation Simulator")

with st.sidebar:
    st.header("Process Inputs")
    preset_label_to_key = {preset.label: key for key, preset in STRAIN_PRESETS.items()}
    preset_label = st.selectbox("Yeast strain", list(preset_label_to_key), index=0)
    preset_key = preset_label_to_key[preset_label]
    preset = STRAIN_PRESETS[preset_key]

    duration_days = st.slider("Fermentation duration (days)", 2.0, 21.0, 7.0, 0.5)
    temperature_c = st.slider(
        "Fermentation temperature (C)",
        0.0,
        42.0,
        float((preset.recommended_min_c + preset.recommended_max_c) / 2.0),
        0.5,
    )
    initial_sugar = st.slider("Initial fermentable sugar (g/L)", 60.0, 240.0, 120.0, 5.0)
    pitch_rate = st.slider("Pitch rate (million cells/mL)", 1.0, 30.0, 9.0, 0.5)
    initial_oxygen = st.slider("Dissolved oxygen at pitch (mg/L)", 0.0, 12.0, 8.0, 0.5)
    aeration_intensity = st.slider("Aeration intensity after pitch (%)", 0, 100, 20, 5)

    with st.expander("Calibration Parameters"):
        mu_multiplier = st.slider("Growth-rate multiplier", 0.50, 1.50, 1.00, 0.05)
        ks = st.slider("Monod Ks (g/L)", 0.1, 2.0, preset.ks, 0.1)
        ethanol_yield = st.slider("Ethanol yield Yps (g/g sugar)", 0.42, 0.51, preset.ethanol_yield, 0.01)
        ethanol_tolerance = st.slider(
            "Ethanol tolerance (% ABV)",
            5.0,
            14.0,
            preset.ethanol_tolerance_abv,
            0.5,
        )
        sugar_uptake_multiplier = st.slider("Sugar uptake multiplier", 0.50, 1.50, 1.00, 0.05)

yeast = YeastKinetics.from_preset(preset_key, mu_multiplier=mu_multiplier).with_updates(
    ks=ks,
    ethanol_yield=ethanol_yield,
    ethanol_tolerance_abv=ethanol_tolerance,
    sugar_uptake_rate=preset.sugar_uptake_rate * sugar_uptake_multiplier,
)
oxygen = OxygenTransferConfig(
    k_la=(aeration_intensity / 100.0) / SECONDS_PER_HOUR,
    saturation_concentration=10.0e-3,
)
vessel = VesselConfig(temperature=temperature_c + 273.15)
quality = QualityConfig()
config = SimulationConfig(
    duration=duration_days * 24.0 * SECONDS_PER_HOUR,
    sample_interval=0.5 * SECONDS_PER_HOUR,
    yeast=yeast,
    oxygen=oxygen,
    vessel=vessel,
    quality=quality,
)
initial_state = make_initial_state(
    substrate=initial_sugar,
    pitch_rate=pitch_rate * 1.0e12,
    dissolved_oxygen=initial_oxygen / 1000.0,
    temperature=temperature_c + 273.15,
)

result = simulate(config=config, initial_state=initial_state)
summary = result.summary
data = make_dataframe(result)

metrics = st.columns(5)
metrics[0].metric("Final ABV", f"{summary.final_abv:.2f}%")
metrics[1].metric("Residual sugar", f"{summary.residual_sugar:.1f} g/L")
metrics[2].metric("Attenuation", f"{summary.attenuation * 100.0:.0f}%")
metrics[3].metric("Viability", f"{summary.final_viability * 100.0:.0f}%")
completion = "Not reached" if summary.completion_time_hours is None else f"{summary.completion_time_hours:.0f} h"
metrics[4].metric("75% sugar used", completion)

tab_main, tab_cells, tab_quality, tab_data, tab_assumptions = st.tabs(
    ["Fermentation", "Yeast", "Oxygen & Quality", "Data", "Assumptions"]
)

with tab_main:
    left, right = st.columns(2)
    left.line_chart(data, x="Time (h)", y=["Sugar (g/L)", "Ethanol (g/L)"])
    right.line_chart(data, x="Time (h)", y="ABV (%)")

with tab_cells:
    st.line_chart(data, x="Time (h)", y=["Viable yeast (million cells/mL)", "Dead yeast (million cells/mL)"])

with tab_quality:
    left, right = st.columns(2)
    left.line_chart(data, x="Time (h)", y="Dissolved oxygen (mg/L)")
    right.line_chart(data, x="Time (h)", y="Flavor retention (%)")

with tab_data:
    st.dataframe(data, width="stretch")

with tab_assumptions:
    st.subheader("Scenario Warnings")
    for flag in summary.risk_flags:
        st.write(f"- {flag}")

    st.subheader("Model Basis")
    st.write(
        "The MVP uses SI-unit ODEs for Monod substrate-limited growth, CTMI temperature response, "
        "ethanol inhibition, stress-adjusted yeast death, sugar-to-ethanol yield, oxygen transfer and uptake, "
        "and first-order flavor degradation. The simulation assumes an isothermal fermenter and should be used "
        "for process sensitivity, education, and model calibration planning rather than batch release decisions."
    )

    st.subheader("Selected Strain Preset")
    st.write(
        {
            "Organism": preset.organism,
            "mu_opt_h^-1": round(yeast.mu_opt * SECONDS_PER_HOUR, 3),
            "Ks_g_L": yeast.ks,
            "Base death rate_h^-1": round(yeast.base_death_rate * SECONDS_PER_HOUR, 4),
            "Lag time_h": round(yeast.lag_time / SECONDS_PER_HOUR, 1),
            "Ethanol tolerance_ABV": yeast.ethanol_tolerance_abv,
            "Yps_g_g": yeast.ethanol_yield,
            "CTMI Tmin/Topt/Tmax_C": (
                preset.temperature_min_c,
                preset.temperature_opt_c,
                preset.temperature_max_c,
            ),
        }
    )
