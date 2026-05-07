# Beer Fermentation Simulator

Interactive Streamlit MVP for exploring how brewing process inputs affect fermentation behavior. The model uses ordinary differential equations for yeast growth, sugar depletion, ethanol formation, oxygen transfer and uptake, yeast viability, and flavor-compound degradation.

This is a process-sensitivity and education tool. It is not validated for production release, quality disposition, or regulatory decisions without strain-specific calibration data.

## What The App Does

The app lets a user change practical fermentation inputs and see the predicted curves update immediately:

- Yeast strain preset: ale, lager, or probiotic yeast
- Fermentation duration
- Fermentation temperature
- Initial fermentable sugar
- Pitch rate
- Dissolved oxygen at pitch
- Aeration intensity after pitch
- Advanced calibration parameters: growth multiplier, Monod Ks, ethanol yield, ethanol tolerance, and sugar uptake multiplier

The main outputs are:

- Sugar over time
- Ethanol and estimated ABV over time
- Viable and dead yeast over time
- Dissolved oxygen over time
- Flavor retention over time
- Final ABV, residual sugar, apparent attenuation, viability, and warning flags

## How To Run

Create and activate a virtual environment if needed:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

Run the command-line smoke simulation:

```bash
python scripts/run_simulation.py
```

Run tests:

```bash
pytest -q
```

## Project Structure

```text
beer_sim/
  config.py              Strain presets, kinetic parameters, SI constants
  engine.py              ODE right-hand side, simulation runner, summary metrics
  state.py               State vector for substrate, cells, ethanol, oxygen, flavor, temperature
  units.py               Unit conversion helpers
  models/
    fermentation.py      Sugar depletion and ethanol formation
    growth.py            Monod growth, CTMI temperature response, inhibition, death
    oxygen.py            Oxygen transfer and oxygen uptake
    heat.py              Arrhenius and Fourier helper equations
    lautering.py         Darcy-law helper equation
    quality.py           Flavor degradation
app.py                   Streamlit interface
scripts/run_simulation.py Command-line smoke run
tests/                   Unit and smoke tests
```

## State Variables

The ODE system tracks:

| Symbol | Code field | Unit | Meaning |
| --- | --- | --- | --- |
| S | substrate | kg/m3, numerically equal to g/L | Fermentable sugar |
| Xt | total_cells | cells/m3 | Total yeast population |
| Xd | dead_cells | cells/m3 | Dead yeast population |
| Xv | viable_cells | cells/m3 | Computed as Xt - Xd |
| P | ethanol | kg/m3, numerically equal to g/L | Ethanol concentration |
| O2 | dissolved_oxygen | kg/m3 | Dissolved oxygen |
| A | flavor_compound | relative concentration | Flavor/aroma retention proxy |
| T | temperature | K | Fermentation temperature |

## Core Theory

### 1. Substrate-Limited Growth

The growth model starts with Monod kinetics:

```text
mu_S = S / (Ks + S)
```

The effective growth rate also includes temperature, ethanol inhibition, lag-phase activity, and a carrying-capacity term:

```text
mu_eff = mu_opt * mu_S * f_T(T) * f_E(P) * f_lag(t)
dXt/dt = mu_eff * Xv * (1 - Xt / Xt_max)
```

### 2. CTMI Temperature Response

Temperature activity uses the Cardinals Temperature Model with Inflection:

```text
f_T(T) =
((T - Tmax) * (T - Tmin)^2)
/
((Topt - Tmin) * ((Topt - Tmin) * (T - Topt)
 - (Topt - Tmax) * (Topt + Tmin - 2T)))
```

The function is normalized so that activity is near 1 at Topt and 0 outside Tmin to Tmax.

### 3. Ethanol Inhibition

As ethanol approaches the strain tolerance, yeast growth is reduced:

```text
f_E = max(1 - (ABV / ABV_tolerance)^2, 0)
```

ABV is estimated from ethanol concentration:

```text
ABV_percent = ethanol_kg_m3 / 789 * 100
```

### 4. Yeast Death

Dead cells accumulate from viable cells:

```text
dXd/dt = kd_eff * Xv
```

The base death rate is increased under high-temperature and high-ethanol stress. This makes hot or high-alcohol scenarios produce lower final viability.

### 5. Sugar Consumption And Ethanol Production

Sugar depletion is biomass-driven and reduced by substrate limitation, temperature, and ethanol stress:

```text
dS/dt = -qS * biomass * mu_S * f_T(T) * f_E(P)
```

Ethanol is produced from sugar consumption:

```text
dP/dt = Yps * (-dS/dt)
```

The default brewing yield is approximately 0.46-0.48 g ethanol per g sugar, below the theoretical maximum of about 0.51 because some sugar supports biomass and side products.

### 6. Oxygen Transfer And Uptake

Dissolved oxygen follows transfer from aeration minus yeast uptake:

```text
dO2/dt = kLa * (O2_sat - O2) - qO2 * biomass_g_m3 * O2 / (KO2 + O2)
```

The default uptake constant is based on the supplied value of about 0.16 micromol O2 per g biomass per minute.

### 7. Flavor Degradation

Flavor retention is represented as a first-order degradation proxy:

```text
dA/dt = -kA(T) * A
```

The temperature dependence uses a Q10 assumption. This is intentionally simple and should be replaced with compound-specific kinetics if the app is used for a specific flavor marker.

## Yeast Presets

| Preset | Organism | mu_opt (h^-1) | Ks (g/L) | Operating temp (C) | CTMI Tmin/Topt/Tmax (C) | Ethanol tolerance (% ABV) | Yps |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ale | Saccharomyces cerevisiae | 0.30 | 1.0 | 18-22 | 3 / 30 / 41 | 10 | 0.48 |
| Lager | Saccharomyces pastorianus | 0.18 | 1.0 | 10-14 | 1 / 22 / 36 | 8 | 0.48 |
| Probiotic | Saccharomyces boulardii | 0.28 | 1.0 | 30-37 | 5 / 37 / 42 | 7 | 0.46 |

These are representative midpoint assumptions from the ranges supplied in `SPEC.md` and the project prompt. They are intentionally centralized in `beer_sim/config.py` so a user can replace them with literature values or fitted lab values.

## Current Assumptions

- The fermenter is isothermal. Temperature is an input, not a solved heat-balance state.
- Sugar is represented as one fermentable substrate pool.
- pH, FAN, osmotic stress, CO2 pressure, yeast flocculation, and nutrient limitation are not yet modeled.
- Biomass is estimated from cell count using a fixed dry mass per cell.
- Oxygen uptake is simplified and does not distinguish respiratory and fermentative phases.
- Flavor degradation is a proxy, not a compound-specific prediction.
- Apparent attenuation is estimated from sugar depletion, not hydrometer gravity.

## How To Make It More Legit

The next scientific improvements should be data-driven:

- Fit ale, lager, and probiotic presets to fermentation datasets.
- Add pH and nutrient limitation terms.
- Add a heat-balance ODE for metabolic heat and cooling control.
- Track original gravity, final gravity, real extract, and apparent extract.
- Add validation plots comparing predicted sugar, ethanol, and viable yeast to lab measurements.
- Replace the flavor proxy with compound-specific kinetics for a selected marker.
