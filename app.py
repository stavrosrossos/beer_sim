"""Interactive Streamlit MVP for fermentation process sensitivity."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from beer_sim.brewing import (
    FERMENTABLE_POTENTIALS_PPG,
    abv_from_gravity,
    apparent_attenuation_from_gravity,
    estimate_final_gravity_from_og,
    extract_g_l_from_sg,
    sg_from_extract_g_l,
    sg_from_recipe,
)
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


def make_dataframe(result, original_gravity: float) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Time (h)": result.time / SECONDS_PER_HOUR,
            "Sugar (g/L)": [state.substrate for state in result.states],
            "Estimated SG": [sg_from_extract_g_l(state.substrate) for state in result.states],
            "Ethanol (g/L)": [state.ethanol for state in result.states],
            "Model ABV (%)": [ethanol_abv(state.ethanol) for state in result.states],
            "Brewing ABV (%)": [
                abv_from_gravity(original_gravity, sg_from_extract_g_l(state.substrate))
                for state in result.states
            ],
            "Biomass (g/L)": [state.biomass for state in result.states],
            "Viable yeast (million cells/mL)": [state.viable_cells / 1.0e12 for state in result.states],
            "Dead yeast (million cells/mL)": [state.dead_cells / 1.0e12 for state in result.states],
            "Dissolved oxygen (mg/L)": [state.dissolved_oxygen * 1000.0 for state in result.states],
            "Flavor retention (%)": [state.flavor_compound * 100.0 for state in result.states],
            "VDK / diacetyl proxy (mg/L)": [state.vdk * 1000.0 for state in result.states],
            "Acetaldehyde proxy (mg/L)": [state.acetaldehyde * 1000.0 for state in result.states],
            "Esters proxy (mg/L)": [state.esters * 1000.0 for state in result.states],
            "Higher alcohols proxy (mg/L)": [state.higher_alcohols * 1000.0 for state in result.states],
            "CO2 produced (g/L)": [state.co2 for state in result.states],
            "Wort temperature (C)": [state.temperature - 273.15 for state in result.states],
            "Jacket temperature (C)": [state.jacket_temperature - 273.15 for state in result.states],
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
    wort_input_mode = st.radio(
        "Wort strength input",
        ["Original Gravity", "Sugar / extract", "Extract recipe"],
        horizontal=False,
    )
    if wort_input_mode == "Original Gravity":
        original_gravity = st.slider("Original Gravity (OG)", 1.020, 1.100, 1.048, 0.001, format="%.3f")
        initial_sugar = extract_g_l_from_sg(original_gravity)
    elif wort_input_mode == "Sugar / extract":
        initial_sugar = st.slider("Initial fermentable sugar / extract (g/L)", 60.0, 240.0, 120.0, 5.0)
        original_gravity = sg_from_extract_g_l(initial_sugar)
    else:
        fermentable = st.selectbox("Fermentable", list(FERMENTABLE_POTENTIALS_PPG), index=0)
        fermentable_weight = st.slider("Fermentable weight (lb)", 1.0, 20.0, 5.0, 0.25)
        batch_volume = st.slider("Batch size (gal)", 1.0, 15.0, 5.0, 0.25)
        default_efficiency = 0.72 if fermentable == "Base grain" else 1.0
        efficiency_percent = st.slider("Brewhouse efficiency (%)", 50, 100, int(default_efficiency * 100), 1)
        original_gravity = sg_from_recipe(
            fermentable_weight,
            FERMENTABLE_POTENTIALS_PPG[fermentable],
            batch_volume,
            efficiency_percent / 100.0,
        )
        initial_sugar = extract_g_l_from_sg(original_gravity)
        st.caption(f"Predicted OG from PPG: {original_gravity:.3f}")

    pitch_rate = st.slider("Pitch rate (million cells/mL)", 5.0, 150.0, 100.0, 5.0)
    initial_oxygen = st.slider("Dissolved oxygen at pitch (mg/L)", 0.0, 12.0, 8.0, 0.5)
    aeration_intensity = st.slider("Aeration intensity after pitch (%)", 0, 100, 20, 5)

    with st.expander("Thermal Model"):
        dynamic_temperature = st.checkbox("Solve heat-balance temperature dynamics", value=False)
        batch_volume_l = st.slider("Batch volume (L)", 5.0, 500.0, 20.0, 5.0)
        heat_transfer_area = st.slider("Cooling area (m2)", 0.05, 5.0, 0.25, 0.05)
        heat_transfer_coefficient = st.slider("Heat transfer coefficient U (W/m2/K)", 0.0, 300.0, 75.0, 5.0)
        coolant_temperature_c = st.slider("Coolant inlet temperature (C)", -5.0, 25.0, 12.0, 0.5)
        coolant_flow_m3_h = st.slider("Coolant flow rate (m3/h)", 0.0, 2.0, 1.4, 0.1)
        jacket_volume_l = st.slider("Jacket volume (L)", 1.0, 100.0, 5.0, 1.0)

    with st.expander("Calibration Parameters"):
        mu_multiplier = st.slider("Growth-rate multiplier", 0.50, 1.50, 1.00, 0.05)
        ks = st.slider("Growth saturation Ksx (g/L)", 1.0, 300.0, preset.ks, 1.0)
        product_ks = st.slider("Product saturation Ksp (g/L)", 50.0, 700.0, preset.product_ks, 5.0)
        q_pmax_h = st.slider("Max ethanol rate qpmax (g/g/h)", 0.10, 2.00, preset.q_pmax * SECONDS_PER_HOUR, 0.05)
        biomass_yield = st.slider("Biomass yield Yxs (g/g sugar)", 0.05, 0.60, preset.biomass_yield, 0.01)
        ethanol_yield = st.slider("Ethanol yield Yps (g/g sugar)", 0.35, 0.51, preset.ethanol_yield, 0.01)
        ethanol_inhibition = st.slider("Aiba ethanol inhibition Kix (L/g)", 0.00, 0.20, preset.ethanol_inhibition, 0.01)
        product_inhibition = st.slider("Product inhibition Kip (L/g)", 0.00, 0.20, preset.product_inhibition, 0.01)
        ethanol_tolerance = st.slider(
            "Ethanol tolerance (% ABV)",
            5.0,
            14.0,
            preset.ethanol_tolerance_abv,
            0.5,
        )

yeast = YeastKinetics.from_preset(preset_key, mu_multiplier=mu_multiplier).with_updates(
    ks=ks,
    product_ks=product_ks,
    q_pmax=q_pmax_h / SECONDS_PER_HOUR,
    biomass_yield=biomass_yield,
    ethanol_yield=ethanol_yield,
    ethanol_inhibition=ethanol_inhibition,
    product_inhibition=product_inhibition,
    ethanol_tolerance_abv=ethanol_tolerance,
)
oxygen = OxygenTransferConfig(
    k_la=(aeration_intensity / 100.0) / SECONDS_PER_HOUR,
    saturation_concentration=10.0e-3,
)
vessel = VesselConfig(
    volume=batch_volume_l / 1000.0,
    temperature=temperature_c + 273.15,
    jacket_temperature=coolant_temperature_c + 273.15,
    coolant_inlet_temperature=coolant_temperature_c + 273.15,
    jacket_volume=jacket_volume_l / 1000.0,
    coolant_flow_rate=coolant_flow_m3_h / SECONDS_PER_HOUR,
    wall_area=heat_transfer_area,
    heat_transfer_coefficient=heat_transfer_coefficient,
    dynamic_temperature=dynamic_temperature,
)
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
    jacket_temperature=coolant_temperature_c + 273.15,
)

result = simulate(config=config, initial_state=initial_state)
summary = result.summary
data = make_dataframe(result, original_gravity)
final_gravity = float(data["Estimated SG"].iloc[-1])
brewing_abv = abv_from_gravity(original_gravity, final_gravity)
gravity_attenuation = apparent_attenuation_from_gravity(original_gravity, final_gravity)
estimated_fg = estimate_final_gravity_from_og(original_gravity)

metrics = st.columns(6)
metrics[0].metric("OG", f"{original_gravity:.3f}")
metrics[1].metric("Estimated FG", f"{final_gravity:.3f}")
metrics[2].metric("Model ABV", f"{summary.final_abv:.2f}%")
metrics[3].metric("Brewing ABV", f"{brewing_abv:.2f}%")
metrics[4].metric("App. attenuation", f"{gravity_attenuation * 100.0:.0f}%")
completion = "Not reached" if summary.completion_time_hours is None else f"{summary.completion_time_hours:.0f} h"
metrics[5].metric("75% sugar used", completion)

secondary_metrics = st.columns(4)
secondary_metrics[0].metric("Residual sugar", f"{summary.residual_sugar:.1f} g/L")
secondary_metrics[1].metric("25% points FG ref.", f"{estimated_fg:.3f}")
secondary_metrics[2].metric("Viability", f"{summary.final_viability * 100.0:.0f}%")
secondary_metrics[3].metric("Final oxygen", f"{summary.final_dissolved_oxygen_mg_l:.1f} mg/L")

flavor_metrics = st.columns(4)
flavor_metrics[0].metric("Peak VDK", f"{summary.peak_vdk_mg_l:.3f} mg/L")
flavor_metrics[1].metric("Final acetaldehyde", f"{summary.final_acetaldehyde_mg_l:.2f} mg/L")
flavor_metrics[2].metric("Esters proxy", f"{summary.final_esters_mg_l:.2f} mg/L")
flavor_metrics[3].metric("Higher alcohols", f"{summary.final_higher_alcohols_mg_l:.2f} mg/L")

thermal_metrics = st.columns(3)
thermal_metrics[0].metric("Peak wort temp", f"{summary.peak_temperature_c:.1f} C")
thermal_metrics[1].metric("Final wort temp", f"{summary.final_temperature_c:.1f} C")
thermal_metrics[2].metric("Final jacket temp", f"{summary.final_jacket_temperature_c:.1f} C")

tab_main, tab_cells, tab_quality, tab_thermal, tab_flavor, tab_data, tab_assumptions = st.tabs(
    ["Fermentation", "Yeast", "Oxygen & Quality", "Thermal", "Flavor", "Data", "Assumptions"]
)

with tab_main:
    left, right = st.columns(2)
    left.line_chart(data, x="Time (h)", y=["Sugar (g/L)", "Ethanol (g/L)"])
    right.line_chart(data, x="Time (h)", y=["Model ABV (%)", "Brewing ABV (%)"])
    st.line_chart(data, x="Time (h)", y="Estimated SG")

with tab_cells:
    left, right = st.columns(2)
    left.line_chart(data, x="Time (h)", y=["Viable yeast (million cells/mL)", "Dead yeast (million cells/mL)"])
    right.line_chart(data, x="Time (h)", y="Biomass (g/L)")

with tab_quality:
    left, right = st.columns(2)
    left.line_chart(data, x="Time (h)", y="Dissolved oxygen (mg/L)")
    right.line_chart(data, x="Time (h)", y="CO2 produced (g/L)")

with tab_thermal:
    st.line_chart(data, x="Time (h)", y=["Wort temperature (C)", "Jacket temperature (C)"])
    st.write(
        {
            "Dynamic heat balance enabled": dynamic_temperature,
            "Batch volume_L": batch_volume_l,
            "Cooling area_m2": heat_transfer_area,
            "U_W_m2_K": heat_transfer_coefficient,
            "Coolant inlet_C": coolant_temperature_c,
            "Coolant flow_m3_h": coolant_flow_m3_h,
        }
    )

with tab_flavor:
    left, right = st.columns(2)
    left.line_chart(data, x="Time (h)", y=["VDK / diacetyl proxy (mg/L)", "Acetaldehyde proxy (mg/L)"])
    right.line_chart(data, x="Time (h)", y=["Esters proxy (mg/L)", "Higher alcohols proxy (mg/L)"])

with tab_data:
    st.dataframe(data, width="stretch")

with tab_assumptions:
    st.subheader("Scenario Warnings")
    for flag in summary.risk_flags:
        st.write(f"- {flag}")

    st.subheader("Model Basis")
    st.write(
        "The simulator uses SI-unit ODEs for a Shopska-style non-structural fermentation engine: "
        "biomass growth follows Monod kinetics with Aiba ethanol inhibition, ethanol is produced through "
        "a biomass-specific product rate, substrate depletion is tied to biomass and ethanol yields, and "
        "secondary metabolite proxies are growth-associated with biomass-dependent cleanup for VDK and "
        "acetaldehyde. Oxygen transfer/uptake and brewing gravity calculations are included. The current "
        "temperature can be held isothermal or solved with a lumped wort/jacket heat balance."
    )

    st.subheader("Gravity Basis")
    st.write(
        {
            "Input mode": wort_input_mode,
            "Original Gravity": round(original_gravity, 3),
            "Final Gravity from residual extract": round(final_gravity, 3),
            "Model ABV from ethanol density": round(summary.final_abv, 2),
            "Brewing ABV from OG-FG": round(brewing_abv, 2),
            "Apparent attenuation from OG-FG": round(gravity_attenuation * 100.0, 1),
        }
    )

    st.subheader("Selected Strain Preset")
    st.write(
        {
            "Organism": preset.organism,
            "mu_opt_h^-1": round(yeast.mu_opt * SECONDS_PER_HOUR, 3),
            "Ksx_g_L": yeast.ks,
            "qpmax_g_g_h": round(yeast.q_pmax * SECONDS_PER_HOUR, 3),
            "Ksp_g_L": yeast.product_ks,
            "Kix_L_g": yeast.ethanol_inhibition,
            "Kip_L_g": yeast.product_inhibition,
            "Yxs_g_g": yeast.biomass_yield,
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
