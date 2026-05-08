# Beer Fermentation Simulator

Interactive Streamlit MVP for exploring how brewing process inputs affect fermentation behavior. The model uses ordinary differential equations for biomass growth, extract depletion, ethanol formation, oxygen transfer and uptake, yeast viability, CO2 production, and secondary flavor-metabolite proxies.

This is a process-sensitivity and education tool. It is not validated for production release, quality disposition, or regulatory decisions without strain-specific calibration data.

## What The App Does

The app lets a user change practical fermentation inputs and see the predicted curves update immediately:

- Yeast strain preset: literature W34/70 lager, ale, lager, or probiotic yeast
- Fermentation duration
- Fermentation temperature
- Wort strength entered as Original Gravity, sugar/extract concentration, or an extract recipe
- Pitch rate
- Dissolved oxygen at pitch
- Aeration intensity after pitch
- Optional heat-balance controls: batch volume, cooling area, heat transfer coefficient, coolant temperature, coolant flow, and jacket volume
- Advanced calibration parameters: growth multiplier, Monod/Aiba constants, biomass yield, ethanol yield, ethanol production rate, and ethanol tolerance

The main outputs are:

- Sugar over time
- Ethanol and estimated ABV over time
- Viable and dead yeast over time
- Dissolved oxygen over time
- CO2 production over time
- Wort and jacket temperature over time when the heat-balance model is enabled
- VDK/diacetyl, acetaldehyde, esters, and higher alcohol proxy curves
- OG, estimated FG, model ABV, brewing ABV, apparent attenuation, residual sugar, viability, and warning flags

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
  brewing.py             Gravity, extract, attenuation, recipe PPG, and brewing ABV helpers
  engine.py              ODE right-hand side, simulation runner, summary metrics
  state.py               State vector for extract, cells, biomass, ethanol, oxygen, flavors, CO2, temperature
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
| X | biomass | kg/m3, numerically equal to g/L | Active yeast biomass |
| P | ethanol | kg/m3, numerically equal to g/L | Ethanol concentration |
| O2 | dissolved_oxygen | kg/m3 | Dissolved oxygen |
| A | flavor_compound | relative concentration | Flavor/aroma retention proxy |
| VDK | vdk | kg/m3 | Vicinal diketone / diacetyl proxy |
| AcA | acetaldehyde | kg/m3 | Acetaldehyde proxy |
| Est | esters | kg/m3 | Ester proxy |
| FA | higher_alcohols | kg/m3 | Higher alcohol proxy |
| CO2 | co2 | kg/m3, numerically equal to g/L | Cumulative CO2 production proxy |
| T | temperature | K | Fermentation temperature |
| Tj | jacket_temperature | K | Cooling jacket temperature |

## Core Theory

### 1. Primary Metabolism

The current fermentation engine follows the non-structural biokinetic model extracted in `knowledge.md`, using biomass, extract, and ethanol as the core dynamic states:

```text
dX/dt = mu X
dP/dt = q X
dS/dt = -(1/Yxs) dX/dt - (1/Yps) dP/dt
```

The growth and product rates use Monod saturation with Aiba-style ethanol inhibition:

```text
mu = mu_max * S/(Ksx + S) * exp(-Kix P) * f_T(T) * f_lag(t)
q = qpmax * S/(Ksp + S) * exp(-Kip P) * f_T(T) * f_lag(t)
```

Here `S`, `X`, and `P` use kg/m3, which is numerically equal to g/L for these concentration terms.

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

The primary kinetic inhibition term is the Aiba exponential:

```text
growth inhibition = exp(-Kix P)
product inhibition = exp(-Kip P)
```

ABV is estimated from ethanol concentration:

```text
ABV_percent = ethanol_kg_m3 / 789 * 100
```

This is shown in the app as `Model ABV`.

### 4. Yeast Death

Dead cells accumulate from viable cells:

```text
dXd/dt = kd_eff * Xv
```

The base death rate is increased under high-temperature and high-ethanol stress. This makes hot or high-alcohol scenarios produce lower final viability.

### 5. Extract Consumption And Ethanol Production

Unlike the earlier simple model, ethanol is not calculated directly as `Yps * sugar consumed`. Ethanol formation first follows a biomass-specific product rate:

```text
dP/dt = q X
```

Extract consumption is then coupled to both biomass growth and ethanol formation:

```text
dS/dt = -(1/Yxs) dX/dt - (1/Yps) dP/dt
```

The default literature W34/70 preset uses `Yxs = 0.47 g/g` and `Yps = 0.43 g/g`, based on the extracted Shopska-style free-cell values for 13 Plato wort.

### 6. Oxygen Transfer And Uptake

Dissolved oxygen follows transfer from aeration minus yeast uptake:

```text
dO2/dt = kLa * (O2_sat - O2) - qO2 * biomass_g_m3 * O2 / (KO2 + O2)
```

The default uptake constant is based on the supplied value of about 0.16 micromol O2 per g biomass per minute.

### 7. Secondary Metabolite Proxies

The app now tracks flavor-relevant proxy states:

```text
dVDK/dt = YVDK * mu * X - kVDK * VDK * X
dAcA/dt = YAcA * mu * X - kAcA * AcA * X
dEst/dt = YEst * mu * X
dFA/dt = YFA * mu * X
```

`VDK` is used as a vicinal diketone/diacetyl proxy. `AcA` is an acetaldehyde proxy. `Est` and `FA` are aggregate ester and higher-alcohol proxies. These equations are growth-associated and are useful for qualitative process comparison, but they should be calibrated before quantitative sensory interpretation.

### 8. CO2 Production

CO2 production is tracked from extract consumption:

```text
dCO2/dt = Yco2/s * (-dS/dt)
```

The default `Yco2/s` is 0.489 g CO2 per g sugar consumed, close to the stoichiometric ethanol/CO2 split for fermentable sugar.

### 9. Brewing Gravity Outputs

The app also reports brewing-native gravity calculations on top of the ODE simulation.

Gravity points are computed from specific gravity:

```text
points = (SG - 1) * 1000
SG = 1 + points / 1000
```

For extract or grain recipes, predicted OG is calculated from potential points per pound per gallon:

```text
gravity_points = pounds * potential_PPG * efficiency / batch_volume_gal
OG = 1 + gravity_points / 1000
```

The included potentials are:

| Fermentable | Potential |
| --- | ---: |
| Dry malt extract (DME) | 44 PPG |
| Liquid malt extract (LME) | 36 PPG |
| Base grain | 37 PPG |

Dilution and boil-off use gravity-point conservation:

```text
points_1 * volume_1 = points_2 * volume_2
```

Brewing-style ABV is calculated from OG and estimated FG:

```text
ABV_percent = (OG - FG) * 131.25
```

Apparent attenuation is calculated as:

```text
attenuation = (OG - FG) / (OG - 1)
```

For display, the simulator approximates extract from SG using Plato:

```text
Plato = -616.868 + 1111.14*SG - 630.272*SG^2 + 135.997*SG^3
extract_g_L approximately Plato * 10
```

Residual sugar from the ODE is converted back to an estimated SG curve using:

```text
SG = 1 + Plato / (258.6 - ((Plato / 258.2) * 227.1))
```

The app intentionally shows both `Model ABV`, from simulated ethanol concentration, and `Brewing ABV`, from OG-FG. These will not always match because the gravity calculation is an empirical brewing approximation while the ODE model explicitly tracks ethanol mass.

### 10. Heat Balance

The app can optionally solve a lumped wort and cooling-jacket heat balance. When disabled, fermentation temperature is held fixed as an operating input. When enabled, the wort temperature becomes a dynamic state.

The wort energy balance is:

```text
dT/dt = (Q_gen - Q_cool) / (rho Cp V)
```

Metabolic heat generation is estimated from extract consumption:

```text
Q_gen = ((-dS/dt) * V / M_glucose) * DeltaH_FG
```

where `DeltaH_FG = 17,500 J/mol`, `M_glucose = 0.180156 kg/mol`, `rho = 1053 kg/m3`, and `Cp = 4180 J/kg/K` by default.

Cooling removal is:

```text
Q_cool = U A (T - Tj)
```

The jacket energy balance is:

```text
dTj/dt = Fc(Tc - Tj)/Vj + Q_cool/(rho_c Cp_c Vj)
```

This is a lumped model, not a CFD model. It assumes a well-mixed bulk wort temperature and a well-mixed jacket temperature. The source extraction also included a log-mean temperature difference form, but the current implementation uses `T - Tj` for stability and because jacket outlet temperature is not explicitly modeled.

## Yeast Presets

| Preset | Organism | mu_max (h^-1) | Ksx (g/L) | qpmax (g/g/h) | Ksp (g/L) | Kix (L/g) | Yxs | Yps |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Literature lager W34/70 | Saccharomyces cerevisiae W34/70 | 0.0222 | 237 | 1.25 | 503 | 0.05 | 0.47 | 0.43 |
| Ale | Saccharomyces cerevisiae | 0.30 | 35 | 1.40 | 120 | 0.08 | 0.20 | 0.48 |
| Lager | Saccharomyces pastorianus | 0.18 | 80 | 1.10 | 180 | 0.10 | 0.18 | 0.48 |
| Probiotic | Saccharomyces boulardii | 0.28 | 40 | 1.00 | 150 | 0.11 | 0.18 | 0.46 |

The W34/70 preset is the most literature-backed default from the extracted NotebookLM material. The ale, lager, and probiotic presets are still representative assumptions and should be treated as calibration starting points.

## Current Assumptions

- By default, the fermenter is isothermal and temperature is held as an input. Heat-balance mode can be enabled in the app.
- If heat-balance mode is enabled, the fermenter and jacket are treated as well-mixed lumped thermal masses.
- Heat generation is estimated from extract consumption using glucose-equivalent heat of fermentation.
- Wort extract is represented as one fermentable substrate pool.
- pH, FAN, osmotic stress, CO2 pressure, yeast flocculation, and nutrient limitation are not yet modeled.
- Biomass is estimated from cell count using a fixed dry mass per cell.
- Oxygen uptake is simplified and does not distinguish respiratory and fermentative phases.
- VDK, acetaldehyde, esters, and higher alcohols are proxy state variables, not validated compound-specific predictions.
- Flavor coefficients are implemented as hidden calibration parameters because the extracted source units and strain dependence need experimental calibration.
- Estimated FG is calculated from residual extract and does not yet correct for alcohol's effect on hydrometer readings.
- Apparent attenuation is reported from estimated OG-FG gravity points.

## How To Make It More Legit

The next scientific improvements should be data-driven:

- Fit ale, lager, and probiotic presets to fermentation datasets.
- Improve the heat-balance model with jacket outlet temperature, log-mean temperature difference, and controller logic.
- Add pH and FAN/amino-acid limitation terms.
- Split extract into glucose, maltose, and maltotriose uptake.
- Add aroma partitioning and CO2 stripping losses.
- Improve final gravity using real/apparent extract equations that account for ethanol density.
- Add validation plots comparing predicted sugar, ethanol, and viable yeast to lab measurements.
- Replace aggregate flavor proxies with compound-specific kinetics for selected markers.
