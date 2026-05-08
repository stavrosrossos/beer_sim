The following mathematical models and parameters have been extracted from the sources and converted to **consistent SI units** (kilograms, metres, seconds, Kelvin, and Joules) where applicable.

### 1. Non-structural Biokinetic Model for Primary Metabolism
1.  **Equation:** 
    $\frac{dX}{dt} = \mu X$
    $\frac{dP}{dt} = q X$
    $\frac{dS}{dt} = -\frac{1}{Y_{x/s}} \frac{dX}{dt} - \frac{1}{Y_{p/s}} \frac{dP}{dt}$
2.  **Plain-English meaning:** A system of ordinary differential equations (ODEs) describing the rates of yeast biomass growth, ethanol product formation, and substrate (sugar) consumption over time.
3.  **Variables and units:** 
    *   $X$: Biomass concentration ($kg \cdot m^{-3}$).
    *   $P$: Ethanol concentration ($kg \cdot m^{-3}$).
    *   $S$: Substrate concentration ($kg \cdot m^{-3}$).
    *   $t$: Time ($s$).
    *   $\mu$: Specific growth rate ($s^{-1}$).
    *   $q$: Specific product accumulation rate ($s^{-1}$).
4.  **Parameter values and units:** 
    *   $\mu_{max}$: $6.1 \times 10^{-6}$ to $1.75 \times 10^{-4} s^{-1}$.
    *   $Y_{x/s}$: 0.47 (Free cells), 0.0154 (Immobilised).
    *   $Y_{p/s}$: 0.43 (Free cells), 1.25 (Immobilised).
5.  **Organism/strain used:** *S. cerevisiae* (strains EC 1118, W34/70, S288c).
6.  **Conditions:** Synthetic media or wort (12–13 °P); Temperature 288.15–303.15 K (15–30 °C); pH 4.0–5.2.
7.  **Experimental scale:** Lab scale (1 L to 15 L) and pilot scale (10 L).
8.  **Process stage:** Primary fermentation.
9.  **Source:** Shopska et al.; Yusupov et al..
10. **Assumptions:** Homogeneous medium; isothermal conditions; single limiting substrate.

---

### 2. Product (Ethanol) Inhibition Models
1.  **Equations:**
    *   **Aiba Model:** $\mu = \mu_{max} \frac{S}{K_{sx} + S} e^{-K_{ix} P}$
    *   **Modified Monod:** $\mu = \mu_{max} \frac{S}{K_{sx} + S + \frac{P^2}{K_{SXi}}}$
2.  **Plain-English meaning:** Modifications to the specific growth rate to account for the toxic effects of accumulated ethanol on yeast cells.
3.  **Variables and units:** 
    *   $K_{ix}$: Inhibition constant ($m^3 \cdot kg^{-1}$).
    *   $K_{SXi}$: Squared inhibition constant ($kg^2 \cdot m^{-6}$).
4.  **Parameter values and units:** 
    *   $K_{ix}$: $0.05 \text{ to } 0.15 \text{ } m^3 \cdot kg^{-1}$ (estimated from graphs for 13 °P wort).
5.  **Organism/strain used:** *S. carlsbergensis* S-23; *S. cerevisiae* S-33.
6.  **Conditions:** Wort extract 9–17 °P.
7.  **Experimental scale:** Laboratory.
8.  **Process stage:** Main fermentation (late stage).
9.  **Source:** Shopska et al..
10. **Assumptions:** Inhibition is primarily driven by ethanol concentration; effects of temperature on inhibition constants are often simplified.

---

### 3. Detailed Multistage Sugar Utilization (Ramirez/Maciejowski)
1.  **Equation:** 
    $\mu_G = \mu_{max,G} \frac{G}{K_G + G}$
    $\mu_M = \mu_{max,M} \frac{M}{K_M + M} \frac{K'_G}{K'_G + G}$
    $\mu_N = \mu_{max,N} \frac{N}{K_N + N} \frac{K'_G}{K'_G + G} \frac{K'_M}{K'_M + M}$
2.  **Plain-English meaning:** A kinetic model describing sequential sugar uptake where glucose ($G$) inhibits maltose ($M$) utilization, and both inhibit maltotriose ($N$) utilization.
3.  **Variables and units:** $G, M, N$: Concentrations of glucose, maltose, and maltotriose ($kg \cdot m^{-3}$).
4.  **Parameter values and units:** 
    *   $\ln \mu_{G0}$: $35.77 \text{ } h^{-1}$ ($9.9 \times 10^{-3} s^{-1}$).
    *   $\tau_D$ (delay): 24.54 h ($8.8 \times 10^4 s$).
5.  **Organism/strain used:** Brewer’s yeast.
6.  **Conditions:** Industrial operational conditions.
7.  **Experimental scale:** Simulations based on industrial data.
8.  **Process stage:** Main fermentation.
9.  **Source:** Ramirez and Maciejowski (via Shopska et al.).
10. **Assumptions:** Sugars are the only limiting nutrients for growth.

---

### 4. Flavor Formation based on CO₂ Evolution
1.  **Equation:** $Alc(t) = Y_{Alc/C} \cdot C_p(t)$
2.  **Plain-English meaning:** The production of aroma compounds (higher alcohols and esters) is directly proportional to the total amount of CO₂ released.
3.  **Variables and units:** 
    *   $Alc(t)$: Aroma compound concentration ($kg \cdot m^{-3}$).
    *   $C_p(t)$: Cumulative CO₂ produced ($m^3_{gas} \cdot m^{-3}_{liquid}$).
    *   $Y_{Alc/C}$: Yield coefficient ($kg_{aroma} \cdot m^{-3}_{CO2}$).
4.  **Parameter values and units (Final Concentrations):**
    *   Isoamyl alcohol: $0.053–0.097 kg \cdot m^{-3}$.
    *   Ethyl acetate: $0.013–0.028 kg \cdot m^{-3}$.
5.  **Organism/strain used:** *S. cerevisiae* var. *uvarum*.
6.  **Conditions:** 283.15–289.15 K (10–16 °C); Top pressure 5–80 kPa (50–800 mbar).
7.  **Experimental scale:** 15 L reactor.
8.  **Process stage:** Batch fermentation.
9.  **Source:** Titica et al..
10. **Assumptions:** CO₂ emission is an online proxy for primary metabolic activity; yield coefficients are constant under constant operating conditions.

---

### 5. Dynamic Heat Transfer Model
1.  **Equation:** $\frac{dT}{dt} = \frac{-X \cdot \Delta H_{FG} \cdot \mu_1}{\rho \cdot C_p} - \frac{U \cdot A \cdot \Delta T_{lm}}{\rho \cdot C_p \cdot V}$
2.  **Plain-English meaning:** The rate of temperature change in the fermenter equals the heat generated by exothermic fermentation minus the heat removed by the cooling jacket.
3.  **Variables and units:** 
    *   $\Delta H_{FG}$: Heat of formation ($J \cdot mol^{-1}$).
    *   $\rho$: Wort density ($kg \cdot m^{-3}$).
    *   $C_p$: Specific heat capacity ($J \cdot kg^{-1}K^{-1}$).
    *   $U$: Heat transfer coefficient ($W \cdot m^{-2}K^{-1}$).
    *   $\Delta T_{lm}$: Log-mean temperature difference ($K$).
4.  **Parameter values and units:** 
    *   Coolant flow rates: $1.2 \text{ to } 1.6 \text{ } m^3 \cdot h^{-1}$.
    *   Pitching rate: $50 \text{ } mol \cdot m^{-3}$.
5.  **Organism/strain used:** Standard brewer's yeast.
6.  **Conditions:** Wort density $1053 kg \cdot m^{-3}$; Initial pH 5.2.
7.  **Experimental scale:** Cylindroconical industrial tank simulation.
8.  **Process stage:** Fermentation cooling control.
9.  **Source:** Tesema et al..
10. **Assumptions:** Cooling jacket is perfectly insulated; wort is a homogeneous liquid; flow is laminar.

---

### 6. Gas-Liquid Partitioning of Aromas
1.  **Equation:** $C_{liq}(t) = \frac{C_{gas}(t)}{k_i}$
2.  **Plain-English meaning:** Describes the equilibrium concentration of a volatile compound in the liquid phase relative to its concentration in the headspace gas.
3.  **Variables and units:** 
    *   $C_{liq}, C_{gas}$: Concentrations ($kg \cdot m^{-3}$).
    *   $k_i$: Partition coefficient (dimensionless).
4.  **Parameter values and units:** Calculated as a function of $E$ (ethanol) and $T$ (temperature) using compound-specific constants $F_1 \text{ to } F_4$.
5.  **Organism/strain used:** Lalvin EC 1118.
6.  **Conditions:** Temperature 291.15–303.15 K (18–30 °C).
7.  **Experimental scale:** 10 L pilot tanks.
8.  **Process stage:** Active fermentation/gas stripping.
9.  **Source:** Mouret et al..
10. **Assumptions:** Instantaneous equilibrium between phases.

---

### 7. Physicochemical Relationships
| Item | Equation Exactly as Written | Variable Definitions | Source |
| :--- | :--- | :--- | :--- |
| **Wort Density** | $^\circ P = \frac{(1000 \cdot d) - 999.448}{4.08745}$ | $^\circ P$: Degrees Plato; $d$: Density | |
| **Dissolved CO₂** | $C_d = 2.96 \times 10^{-6} (P + 1000)(T + 273.16) e^{-0.0335T}$ | $C_d$: $L/L_{wort}$; $P$: $mbar$; $T$: $^\circ C$ | |
| **ABV %** | $ABV = (OG - FG) \cdot 131.25$ | $OG, FG$: Original/Final Gravity | |
| **Nitrogen Contribution** | $f_i^{AA}(t) = 1 - [f_i^{YH}(t) + f_i^{NH3}(t)]$ | $f_i$: Fractional labelling of amino acid $i$ | |

Based on the provided sources, the following ordinary differential equations (ODEs) and time-dependent rate equations describe various aspects of the brewing and fermentation process.

### 1. Primary Metabolism Model (Biomass, Product, and Substrate)
This non-structural model describes the fundamental dynamics of yeast growth and its direct relationship to ethanol production and sugar consumption.

*   **State Variables:** Biomass concentration ($X$), Ethanol concentration ($P$), Substrate/Extract concentration ($S$).
*   **Independent Variable:** Time ($t$).
*   **Full Equations:**
    *   $\frac{dX}{dt} = \mu X$
    *   $\frac{dP}{dt} = q X$
    *   $\frac{dS}{dt} = -\frac{1}{Y_{x/s}} \frac{dX}{dt} - \frac{1}{Y_{p/s}} \frac{dP}{dt}$
*   **Initial Conditions:** $X(0) = X_0$ (Inoculum size); $P(0) = 0$; $S(0) = S_{init}$ (Initial wort extract, e.g., $130 \, g/dm^3$).
*   **Units:**
    *   **State Variables:** $g/dm^3$ or $kg/m^3$.
    *   **Rate Constants:** $\mu$ (specific growth rate) and $q$ (specific product rate) are in $h^{-1}$ or $s^{-1}$.
    *   **Yield Coefficients:** $Y_{x/s}$ and $Y_{p/s}$ are dimensionless ($g/g$).
*   **Parameter Values (at 15 °C):**
    *   **Free Cells:** $\mu_{max} = 0.0222 \, h^{-1}$; $K_{sx} = 237 \, g/dm^3$; $q_{pmax} = 1.25 \, g/(g \cdot h)$; $K_{sp} = 503 \, g/dm^3$; $Y_{x/s} = 0.47$; $Y_{p/s} = 0.43$.
    *   **Immobilised Cells:** $\mu_{max} = 0.012 \, h^{-1}$; $K_{sx} = 39.15 \, g/dm^3$; $q_{pmax} = 10.83 \, g/(g \cdot h)$; $K_{sp} = 323.15 \, g/dm^3$; $Y_{x/s} = 0.0154$; $Y_{p/s} = 1.25$.
*   **Equation Type:** Mechanistic (Monod-based).
*   **Measured Data:** Lab-scale fermentation data using *S. cerevisiae* W34/70 in 13 °P wort.
*   **Reference:** Shopska et al., Page 543–545, Eq. (13.1, 13.2), Table 13.1.

---

### 2. Secondary Metabolite Formation (Flavours)
These equations model the synthesis of compounds that define beer aroma, such as higher alcohols and esters.

*   **State Variables:** Higher alcohol concentration ($FA$), Ester concentration ($E$), Aldehyde concentration ($A$), Vicinal diketone concentration ($VDK$).
*   **Independent Variable:** Time ($t$).
*   **Full Equations:**
    *   $\frac{dFA}{dt} = Y_{FA} \cdot \mu \cdot X(t)$
    *   $\frac{dE}{dt} = Y_E \cdot \mu \cdot X(t)$
    *   $\frac{dA}{dt} = Y_A \cdot \mu \cdot X(t) - k_A \cdot A \cdot X$
    *   $\frac{dVDK}{dt} = Y_{VDK} \cdot \mu(t, T) \cdot X(t, T) - k_{x, VDK} \cdot VDK(t, T) \cdot X(t, T)$
*   **Initial Conditions:** Metabolite concentrations are typically zero at $t=0$.
*   **Units:**
    *   **State Variables:** $mg/dm^3$.
    *   **Yield/Reduction coefficients:** $Y_{FA}, Y_E, Y_A, Y_{VDK}$ in $mg/(g \cdot h)$; $k_A, k_{VDK}$ in $mg/(g \cdot h)$.
*   **Parameter Values (at 15 °C for Free Cells):** $Y_A = 0.1177$; $k_A = 0.0136$; $Y_E = 0.1732$; $Y_{FA} = 0.0733$; $Y_{VDK} = 0.0065$; $K_{VDK} = 0.0285$.
*   **Equation Type:** Mechanistic/Growth-associated.
*   **Measured Data:** Validated against laboratory fermentation kinetics.
*   **Reference:** Shopska et al., Page 545, 557, Table 13.1, Table 13.5.

---

### 3. Detailed Multistage Sugar Utilization
This model explicitly separates the uptake of glucose, maltose, and maltotriose.

*   **State Variables:** Glucose ($G$), Maltose ($M$), Maltotriose ($N$).
*   **Independent Variable:** Time ($t$).
*   **Full Equations:**
    *   $\frac{dG}{dt} = -\mu_1 X$
    *   $\frac{dM}{dt} = -\mu_2 X$
    *   $\frac{dN}{dt} = -\mu_3 X$
*   **Units:** $mol/m^3$ for concentrations; $s$ or $h$ for time.
*   **Parameter Values:** $\ln \mu_{G0} = 35.77 \, h^{-1}$; $\ln \mu_{M0} = 16.4 \, h^{-1}$; $\ln \mu_{N0} = 10.59 \, h^{-1}$.
*   **Equation Type:** Mechanistic/Sequential inhibition.
*   **Measured Data:** Industrial operational data.
*   **Reference:** Ramirez and Maciejowski (via Shopska et al.), Page 550, Table 13.2.

---

### 4. Nutrient (Amino Acid) Consumption
Describes the rate at which specific amino acids are utilized for protein synthesis and flavour precursor formation.

*   **State Variables:** Leucine ($L$), Isoleucine ($I$), Valine ($V$).
*   **Independent Variable:** Time ($t$).
*   **Full Equation (General):** $\frac{dL}{dt} = -Y_{LX} \cdot \frac{dX}{dt} \cdot \frac{L}{K_L + L} \cdot D$
*   **Initial Conditions:** $L_0 = 1.3 \, mol/m^3$; $I_0 = 0.6 \, mol/m^3$; $V_0 = 2.1 \, mol/m^3$.
*   **Units:** $mol/m^3$.
*   **Parameter Values:** $Y_{LX} = 0.0832$; $Y_{IX} = 0.0363$; $Y_{VX} = 0.0273$; $\tau_D = 24.54 \, h$.
*   **Equation Type:** Mechanistic with empirical time delay ($D = 1 - e^{-t/\tau_D}$).
*   **Measured Data:** Validated through simulation and comparison with yeast growth profiles.
*   **Reference:** Tesema et al., Page 11, Eq. (7–9); Ramirez and Maciejowski, Table 13.3.

---

### 5. Dynamic Heat Transfer
Models the temperature change in the fermenter due to metabolic heat generation and external cooling.

*   **State Variable:** Temperature ($T$).
*   **Independent Variable:** Time ($t$).
*   **Full Equation:** $\frac{dT}{dt} = \frac{F_c(T_c - T_j)}{V_j} + \frac{U \cdot A \cdot \Delta T_{lm}}{\rho_c \cdot V_j \cdot C_{pc}}$
*   **Initial Condition:** $T(0) = T_{init}$ (e.g., 20 °C).
*   **Units:** Kelvin ($K$) or Celsius ($^\circ C$).
*   **Equation Type:** Mechanistic (Energy balance).
*   **Measured Data:** Compared with experimental temperature profiles along the tank arc length at a 1.4 $m^3/h$ coolant flow rate.
*   **Reference:** Tesema et al., Page 6, Eq. (2).

---

### 6. Segregated Growth Model (Lag/Active/Dead Cells)
This model accounts for the population dynamics immediately after wort inoculation.

*   **State Variables:** Suspended cells ($X_{sus}$), Active cells ($X_{act}$), Lag-phase cells ($X_{lag}$), Dead cells ($X_{dea}$).
*   **Independent Variable:** Time ($t$).
*   **Full Equations:**
    *   $\frac{dX_{sus}}{dt} = -\mu_{SD} \cdot X_{DT}(t)$
    *   $\frac{dX_{act}}{dt} = \mu_L \cdot X_{lag}$ (for $t < t_{lag}$)
    *   $\frac{dX_{act}}{dt} = \mu_X \cdot X_{act} - \mu_{DT} \cdot X_{act} + \mu_L \cdot X_{lag}$ (for $t > t_{lag}$)
*   **Initial Condition:** $X_{act}(0) + X_{lag}(0) = 0.5 \cdot X_{inc}(0)$.
*   **Units:** Cells per unit volume ($L^{-1}$ or $m^{-3}$).
*   **Equation Type:** Mechanistic/Segregated.
*   **Measured Data:** Industrial Operational Conditions.
*   **Reference:** de Andres-Toro et al. (via Shopska et al.), Page 554, Table 13.4.

The following table consolidates key mathematical parameters for simulating beer fermentation, yeast metabolism, and heat transfer. These values are extracted directly from the sources and are structured for use in computational models (e.g., Python using SciPy's `solve_ivp`).

### Consolidated Parameter Table for Fermentation Simulation

| parameter_name | symbol | value | min | max | unit | equation_used_in | organism_or_strain | beer_style_or_medium | temperature_C | pH | source_paper | page_table_figure | notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Max specific growth rate | $\mu_{max}$ | 0.0222 | — | — | $h^{-1}$ | $dX/dt = \mu X$ | *S. cerevisiae* W34/70 | 13 °P Wort | 15 | — | Shopska et al. | p. 545, Table 13.1 | For free-cell primary metabolism. |
| Saturation constant (growth) | $K_{sx}$ | 237 | — | — | $g/dm^3$ | $\mu = \mu_{max} \frac{S}{K_{sx} + S}$ | *S. cerevisiae* W34/70 | 13 °P Wort | 15 | — | Shopska et al. | p. 545, Table 13.1 | |
| Max specific ethanol rate | $q_{pmax}$ | 1.25 | — | — | $g/(g \cdot h)$ | $dP/dt = q X$ | *S. cerevisiae* W34/70 | 13 °P Wort | 15 | — | Shopska et al. | p. 545, Table 13.1 | |
| Saturation constant (product) | $K_{sp}$ | 503 | — | — | $g/dm^3$ | $q = q_{pmax} \frac{S}{K_{sp} + S}$ | *S. cerevisiae* W34/70 | 13 °P Wort | 15 | — | Shopska et al. | p. 545, Table 13.1 | |
| Yield (biomass/substrate) | $Y_{x/s}$ | 0.47 | — | — | $g/g$ | $dS/dt$ balance | *S. cerevisiae* W34/70 | 13 °P Wort | 15 | — | Shopska et al. | p. 545, Table 13.1 | |
| Yield (ethanol/substrate) | $Y_{p/s}$ | 0.43 | — | — | $g/g$ | $dS/dt$ balance | *S. cerevisiae* W34/70 | 13 °P Wort | 15 | — | Shopska et al. | p. 545, Table 13.1 | |
| Inhibition constant (growth) | $K_{ix}$ | 0.1 | 0.05 | 0.17 | $dm^3/g$ | $\mu \cdot e^{-K_{ix}P}$ | *S. carlsbergensis* S-23 | 9–17 °P Wort | 15 | — | Shopska et al. | p. 548, Fig 13.5 | Product inhibition (Aiba model). |
| Inhibition constant (product) | $K_{ip}$ | 0.08 | 0.02 | 0.22 | $dm^3/g$ | $q \cdot e^{-K_{ip}P}$ | *S. carlsbergensis* S-23 | 9–17 °P Wort | 15 | — | Shopska et al. | p. 548, Fig 13.5 | |
| Frequency factor (Glucose) | $\ln \mu_{G0}$ | 35.77 | — | — | $\ln(h^{-1})$ | Arrhenius $\mu_i$ | Brewer's Yeast | Industrial Wort | — | — | Ramirez (via Shopska) | p. 553, Table 13.3 | Kinetic factor for glucose uptake. |
| Frequency factor (Maltose) | $\ln \mu_{M0}$ | 16.4 | — | — | $\ln(h^{-1})$ | Arrhenius $\mu_i$ | Brewer's Yeast | Industrial Wort | — | — | Ramirez (via Shopska) | p. 553, Table 13.3 | |
| Amino acid delay constant | $\tau_D$ | 24.54 | — | — | $h$ | $D = 1 - e^{-t/\tau_D}$ | Brewer's Yeast | Industrial Wort | — | — | Ramirez (via Shopska) | p. 553, Table 13.3 | Consumption delay for Group B amino acids. |
| Yield (Leucine/Biomass) | $Y_{LX}$ | 0.0832 | — | — | $mol/mol$ | $dL/dt$ balance | Brewer's Yeast | Industrial Wort | — | — | Ramirez (via Shopska) | p. 553, Table 13.3 | |
| Yield (Valine/Biomass) | $Y_{VX}$ | 0.0273 | — | — | $mol/mol$ | $dV/dt$ balance | Brewer's Yeast | Industrial Wort | — | — | Ramirez (via Shopska) | p. 553, Table 13.3 | |
| Wort Density | $\rho$ | 1053 | 1048 | 1070 | $kg/m^3$ | Energy balance | — | 13 °P Wort | — | — | Tesema et al. | p. 13, Symbols | |
| Specific Heat (Wort) | $C_p$ | 4.18 | — | — | $kJ/(kg \cdot ^\circ C)$ | $dT/dt$ balance | — | Beer Wort | — | — | Tesema et al. | p. 12, Symbols | |
| Heat of Formation (Glucose) | $\Delta H_{FG}$ | 17.5 | — | — | $kJ/mol$ | $dT/dt$ balance | — | — | — | — | Tesema et al. | p. 11, Symbols | Overall heat of fermentation. |
| Partition Coeff (Isoamyl Acetate) | $k_i$ | 130 | — | — | — | $C_{liq} = C_{gas}/k_i$ | *S. cerevisiae* | Synthetic Medium | 24 | 4.0 | Mouret et al. | p. 3, Eq (1) | Varies with ethanol % and T. |
| Aroma Yield (Ethyl Acetate) | $Y_{Est/C,1}$ | 0.2652 | 0.03 | 1.04 | $mg/L_{CO2}$ | $Est(t) = Y \cdot C_p$ | *S. cerevisiae* | 13.3 °P Wort | 13 | — | Titica et al. | p. 172, Table VI | Yield relative to CO2 production. |
| Growth rate (Enological) | $k_1(T)$ | 0.31 | 0.14 | 0.48 | $h^{-1}$ | Logistic Growth | Lalvin EC1118 | Glucose (200 g/L) | 18–30 | 4.0 | Malherbe et al. | p. 268, Fig 10 | $k_1 = 0.0287T - 0.3762$. |
| Affinity (Sugar Transport) | $K_s$ | 15 | — | — | $g/L$ | $r_{ST}$ transport | Lalvin EC1118 | Enological must | 24 | 4.0 | Malherbe et al. | p. 270, Eq (1) | Affinity constant for hexose transporters. |

### Practical Simulation Notes
1.  **Temperature Dependence:** For dynamic temperature simulations, replace static values with the **Arrhenius equation** or linear correlations provided in the "notes" or source text (e.g., $k_1(T)$ for growth in wine).
2.  **Inhibition:** When modeling high-gravity brewing (>15 °P), use the **Aiba or Ghose models** to account for ethanol toxicity as concentrations exceed 40–50 g/L.
3.  **Units:** Ensure substrate ($S$) and biomass ($X$) units match the rate constant units (e.g., if using $g/dm^3$, use $h^{-1}$ for rates). Standard SI units ($kg, m^3, s$) are recommended for consistency in multi-physics models.

The following equations and parameters have been converted to **SI-compatible units** for implementation in a computational model (e.g., Python). 

### **Unit Conversion Reference**
| Quantity | Original Unit | SI Unit | Conversion Factor |
| :--- | :--- | :--- | :--- |
| **Time** ($t$) | Hour ($h$) | Second ($s$) | $1 \, h = 3,600 \, s$ |
| **Mass/Conc** ($S, X, P$) | Gram per liter ($g/L$ or $g/dm^3$) | Kilogram per cubic meter ($kg/m^3$) | $1 \, g/L = 1 \, kg/m^3$ |
| **Trace Conc** | Milligram per liter ($mg/L$) | Kilogram per cubic meter ($kg/m^3$) | $1 \, mg/L = 10^{-3} kg/m^3$ |
| **Temperature** ($T$) | Celsius ($^\circ C$) | Kelvin ($K$) | $T(K) = T(^\circ C) + 273.15$ |
| **Pressure** ($P$) | Millibar ($mbar$) | Pascal ($Pa$) | $1 \, mbar = 100 \, Pa$ |
| **Cell Count** ($X$) | Cells per milliliter ($cells/mL$) | Cells per cubic meter ($cells/m^3$) | $1 \, cell/mL = 10^6 \, cells/m^3$ |
| **Energy/Heat** | Kilojoule ($kJ$) | Joule ($J$) | $1 \, kJ = 1,000 \, J$ |

---

### **1. Primary Metabolism (Non-structural Biokinetic Model)**
This model governs the rate of fermentation engine.

*   **Original Equations ($h, g/dm^3$):**
    *   $\frac{dX}{dt} = \mu X$; $\frac{dP}{dt} = q X$
    *   $\mu = \mu_{max} \frac{S}{K_{sx} + S} e^{-K_{ix} P}$
*   **SI-Converted Equations ($s, kg/m^3$):**
    *   $\frac{dX}{dt} = \mu X$; $\frac{dP}{dt} = q X$
    *   $\mu = \mu_{max, SI} \frac{S}{K_{sx} + S} e^{-K_{ix} P}$
*   **Parameters:**
    *   **$\mu_{max}$:** $0.0222 \, h^{-1} \rightarrow \mathbf{6.16 \times 10^{-6} \, s^{-1}}$
    *   **$q_{pmax}$:** $1.25 \, g/(g \cdot h) \rightarrow \mathbf{3.47 \times 10^{-4} \, kg/(kg \cdot s)}$
    *   **$K_{sx}$:** $237 \, g/dm^3 \rightarrow \mathbf{237 \, kg/m^3}$
    *   **$K_{ix}$:** $0.1 \, dm^3/g \rightarrow \mathbf{0.1 \, m^3/kg}$

---

### **2. Secondary Metabolite Formation (Flavor Dynamics)**
Models the accumulation and reduction of diacetyl, aldehydes, and esters.

*   **Original Equations ($h, mg/dm^3$):**
    *   $\frac{dVDK}{dt} = Y_{VDK} \mu X - k_{VDK} VDK \cdot X$
*   **SI-Converted Equations ($s, kg/m^3$):**
    *   $\frac{dVDK}{dt} = Y_{VDK} \mu X - k_{VDK, SI} VDK \cdot X$
*   **Parameters (Free cells at 15 °C):**
    *   **$Y_{VDK}$:** $0.0065 \, mg/g \rightarrow \mathbf{0.0065 \, kg/kg}$ (Dimensionless ratio remains same)
    *   **$k_{VDK}$:** $0.0285 \, mg/(g \cdot h) \rightarrow \mathbf{7.92 \times 10^{-9} \, kg/(kg \cdot s)}$
    *   **$Y_{A}$ (Aldehyde yield):** $0.1177 \rightarrow \mathbf{0.1177 \, kg/kg}$
    *   **$k_{A}$ (Aldehyde reduction):** $0.0136 \, mg/(g \cdot h) \rightarrow \mathbf{3.78 \times 10^{-9} \, kg/(kg \cdot s)}$

---

### **3. Tank Thermodynamics (Heat Transfer)**
The energy balance used to control the cooling jacket.

*   **Original Equation ($^\circ C, kJ/mol, kJ/kg \cdot ^\circ C$):**
    *   $\frac{dT}{dt} = \frac{-X \cdot \Delta H_{FG} \cdot \mu_1}{\rho \cdot C_p} - \frac{U \cdot A \cdot \Delta T_{lm}}{\rho \cdot C_p \cdot V}$
*   **SI-Converted Equation ($K, J/mol, J/kg \cdot K$):**
    *   $\frac{dT}{dt} = \frac{-X \cdot \Delta H_{FG, SI} \cdot \mu_{1, SI}}{\rho \cdot C_{p, SI}} - \frac{U \cdot A \cdot \Delta T_{lm, K}}{\rho \cdot C_{p, SI} \cdot V}$
*   **Parameters:**
    *   **$\Delta H_{FG}$ (Heat of fermentation):** $17.5 \, kJ/mol \rightarrow \mathbf{17,500 \, J/mol}$
    *   **$C_p$ (Specific heat):** $4.18 \, kJ/kg \cdot ^\circ C \rightarrow \mathbf{4,180 \, J/kg \cdot K}$
    *   **$\rho$ (Wort density):** $1053 \, kg/m^3$ (Already SI)
    *   **$U$ (Heat transfer coeff):** $W/m^2 \cdot ^\circ C \rightarrow \mathbf{W/m^2 \cdot K}$ (Numeric value unchanged)

---

### **4. Physicochemical & Aroma Partitioning**
Determining alcohol content and gas-phase losses.

*   **Ethanol by Volume (ABV):**
    *   **Original:** $ABV = (OG - FG) \times 131.25$
    *   **SI Implementation:** Use Specific Gravity ($kg/m^3$ relative to water) directly. No conversion needed for the factor if using standard gravity points.
*   **Dissolved CO₂ ($C_d$):**
    *   **Original ($mbar, ^\circ C$):** $C_d = 2.96 \times 10^{-6} (P + 1000)(T + 273.16) e^{-0.0335T}$
    *   **SI Implementation ($Pa, K$):** $C_d = 2.96 \times 10^{-6} (\frac{P}{100} + 1000)(T_{Kelvin}) e^{-0.0335(T_{Kelvin}-273.15)}$
*   **Aroma Partition Coefficient ($k_i$):**
    *   **Original:** $E$ in $g/L$, $T$ in $K$.
    *   **SI Implementation:** $E$ in $kg/m^3$ (numerical value is identical), $T$ in $K$.
    *   **Example (Ethyl Octanoate):** $F_1 = -3.13, F_2 = -1.35 \times 10^{-2}, F_3 = 52, F_4 = -3.6 \times 10^{-3}$.

---

### **5. Nutrient Limitation (Nitrogen & Amino Acids)**
*   **Assimilable Nitrogen ($N$):**
    *   **Original:** $mg/L$.
    *   **SI:** $\mathbf{10^{-3} \, kg/m^3}$.
*   **Nitrogen-Limited Carrying Capacity ($X_{max}$):**
    *   **Original:** $cells/L$.
    *   **SI Implementation:** $X_{max, SI} = X_{max, orig} \times 1,000$ (to get $cells/m^3$).
    *   **Coefficient Polynomial:** $X_{max}(N_{init}) = 10^9 (-649 N_{init}^2 + 698 N_{init} + 7)$.
        *   If $N_{init}$ is in $kg/m^3$, coefficients must be adjusted. It is safer to calculate in $g/L$ inside the function and multiply result by 1,000.

For a beer fermentation simulator MVP (Minimum Viable Product), the goal is to balance biological accuracy with computational simplicity and parameter availability. Based on the sources, the following equations are recommended for implementation, ranked by priority.

### **1. Core Primary Metabolism (The Engine)**
**Equations:** Non-structural ODEs for Biomass ($X$), Substrate ($S$), and Ethanol ($P$) using Monod kinetics with Aiba product inhibition.
*   **Scientific Credibility:** **Very High.** This is the industry standard for bioprocess modeling.
*   **Availability of Parameters:** **High.** Table 13.1 in Shopska et al. provides complete values for $\mu_{max}$, $K_{sx}$, $Y_{x/s}$, etc., specifically for *S. cerevisiae* W34/70.
*   **Ease of Implementation:** **High.** Requires only three coupled ODEs solvable with `scipy.integrate.solve_ivp`.
*   **Relevance to Beer:** **Critical.** Describes the fundamental transformation of wort into beer.
*   **Calibration Data:** **Minimal.** Only requires initial wort gravity (Plato) and pitching rate.
*   **Risk:** **Low.** These are mechanistic equations with low risk of overfitting.

---

### **2. Sequential Sugar Utilization (The "Beer" Logic)**
**Equations:** Ramirez and Maciejowski’s multi-stage sugar utilization models.
*   **Scientific Credibility:** **High.** Published in the *Journal of the Institute of Brewing*.
*   **Availability of Parameters:** **High.** Complete frequency factors and activation energies for glucose, maltose, and maltotriose are provided in Table 13.3.
*   **Ease of Implementation:** **Medium.** Expands the single substrate ODE into three, adding cross-inhibition terms (e.g., glucose inhibits maltose).
*   **Relevance to Beer:** **Critical.** This is the primary differentiator between wine and beer simulations; beer yeast consumes sugars in a specific order.
*   **Calibration Data:** **Required.** Needs the specific sugar profile of the wort.
*   **Risk:** **Moderate.** Assumes standard inhibition constants that may vary with specific high-gravity worts.

---

### **3. Tank Energy Balance (The Physics)**
**Equations:** Exothermic heat generation and cooling jacket heat transfer ODEs.
*   **Scientific Credibility:** **High.** Based on fundamental laws of thermodynamics (Fourier/Convection).
*   **Availability of Parameters:** **High.** Specific heat capacity ($C_p$), density ($\rho$), and heat of formation ($\Delta H_{FG}$) are well-defined for wort.
*   **Ease of Implementation:** **High.** One ODE for the wort temperature and one for the jacket.
*   **Relevance to Beer:** **Critical.** Fermentation is highly temperature-sensitive; temperature control is the brewer's primary lever for flavor.
*   **Calibration Data:** **Low.** Requires only tank geometry and coolant flow rates.
*   **Risk:** **Very Low.** Mechanistic physical model.

---

### **4. Vicinal Diketone (Diacetyl) Dynamics (The Quality Gate)**
**Equations:** Growth-associated formation and biomass-associated reduction of VDKs.
*   **Scientific Credibility:** **Moderate/High.** Uses growth-associated yield coefficients ($Y_{VDK}$) and reduction constants ($k_{VDK}$).
*   **Availability of Parameters:** **Medium.** Values provided for free cells at 15 °C in Table 13.1.
*   **Ease of Implementation:** **Medium.** One ODE that depends on the primary growth rate $\mu$.
*   **Relevance to Beer:** **High.** Diacetyl is the most important off-flavor in beer; its reduction determines packaging time.
*   **Calibration Data:** **High.** Reduction is highly strain-dependent and temperature-dependent.
*   **Risk:** **Moderate.** Simplifies a complex chemical/biological two-step process into a single reduction term.

---

### **5. Fermentative Aroma Prediction (The Proxy)**
**Equations:** CO₂ emission-based yield relationships for esters and higher alcohols.
*   **Scientific Credibility:** **High.** Validated at 15-L and industrial scales.
*   **Availability of Parameters:** **High.** Extensive tables for isoamyl alcohol, phenyl ethanol, and ethyl acetate provided.
*   **Ease of Implementation:** **High.** Algebraic relationships based on the cumulative integral of CO₂ (which can be derived from the $S \rightarrow P$ conversion).
*   **Relevance to Beer:** **Medium/High.** Essential for predicting the sensory profile of the MVP output.
*   **Calibration Data:** **Low.** Uses online CO₂ measurement as a proxy, which is the easiest state to track.
*   **Risk:** **Moderate.** These are empirical correlations ($Y = aX + b$); while powerful, they can overfit if operating conditions (pressure/temp) move outside the 10–16 °C range.

---

### **Prioritized Implementation List for MVP**

1.  **Phase 1 (The Engine):** Implement the **Priority 1 (Monod/Aiba)** and **Priority 3 (Heat Balance)** equations first. This creates a simulator that can predict gravity drops and temperature curves—the "table stakes" for any brewer.
2.  **Phase 2 (The Beer Reality):** Layer in **Priority 2 (Ramirez Sequential Sugar)**. This makes the gravity curve realistic for wort rather than a generic sugar solution.
3.  **Phase 3 (The Sensory Layer):** Add **Priority 5 (CO₂ Aroma Yields)** and **Priority 4 (Diacetyl)**. This allows the simulator to output flavor "warnings" or "milestones" to the user.

Across the provided sources, the mathematical description of beer fermentation exhibits significant variety in model structure, parameter values, and underlying assumptions. The following comparison identifies the key conflicts and differences.

### **1. Comparison of Primary Metabolism Equations**

| Feature | **Shopska et al.** | **Ramirez / Tesema** | **Malherbe et al.** | **Yusupov et al.** |
| :--- | :--- | :--- | :--- | :--- |
| **Model Type** | Non-structural Monod | Detailed Multistage | Logistic Growth | Non-structural Monod |
| **Biomass ($X$)** | $\frac{dX}{dt} = \mu X$ | $\frac{dX}{dt} = \sum (\text{sugar yields})$ | $\frac{dX}{dt} = k_1 X (1 - \frac{X}{X_{max}})$ | $\frac{dX}{dt} = (\mu - k_d)X$ |
| **Substrate ($S$)** | Unified "Extract" | Glucose, Maltose, Maltotriose | Glucose (Wine must) | Unified "Substrate" |
| **Product ($P$)** | $\frac{dP}{dt} = q X$ | Linear yield from sugars | Gay-Lussac constant yield | $\frac{dP}{dt} = q X$ |
| **Growth Rate ($\mu$)** | Monod + Aiba Inhib. | Arrhenius + Cross-inhib. | Linear $f(T)$ | Monod + Non-competitive |

**Key Conflict:** **Model Topology.** Shopska and Yusupov treat wort as a single substrate, while Ramirez/Tesema model the sequential uptake of individual sugars. Malherbe uses a **logistic model** which, unlike Monod, does not explicitly depend on instantaneous substrate concentration but rather a carrying capacity ($X_{max}$) determined by initial nitrogen.

### **2. Differences in Inhibition Modeling**
The papers propose different mathematical "penalties" for ethanol accumulation:
*   **Exponential (Aiba):** $\mu = \mu_{0} e^{-K_{ix}P}$ (Shopska). This suggests inhibition starts immediately and increases exponentially.
*   **Non-competitive:** $\mu = \mu_{0} / (1 + \frac{P}{K_i})$ (Yusupov). Common in control theory for simplicity.
*   **Linear/Threshold (Ghose):** $\mu = \mu_{0} (1 - \frac{P}{P_{max}})$ (Shopska). Suggests a hard limit where growth stops entirely.
*   **Quadratic Substrate:** $\mu = \mu_{0} \frac{S}{K_{sx} + S + S^2/K_{SXi}}$ (Shopska). Used specifically to model the "dampening" of fermentation in high-gravity worts.

### **3. Conflicts in Parameter Values and Units**

| Parameter | Source 2 (Shopska) | Source 6 (Tesema) | Source 7 (Malherbe) |
| :--- | :--- | :--- | :--- |
| **Saturation ($K_s$)** | $237 \, g/dm^3$ (Extract) | — | $15 \, g/L$ (Hexose) |
| **Units for $S$** | $g/dm^3$ (equiv to $g/L$) | $mol/m^3$ | $g/L$ |
| **Growth Rate ($\mu$)** | $0.0222 \, h^{-1}$ | Calculated via Arrhenius | $0.0287 T - 0.3762$ |
| **Yield ($Y_{x/s}$)** | $0.47 \, g/g$ | mole/mole | (Yield not used in Logistic) |

**Significant Difference:** The **$K_{sx}$ (saturation constant)** in Shopska is exceptionally high ($237 \, g/dm^3$). In contrast, Malherbe identifies an affinity constant of $15 \, g/L$ for sugar transporters. This conflict stems from what the constant represents: Shopska’s value is a "fit" for overall wort extract attenuation, while Malherbe’s is a physiological measure of hexose transport.

### **4. Organisms and Conditions**
*   **Top vs. Bottom Fermentation:** Shopska and Roberts emphasize that *S. cerevisiae* (Ale) and *S. pastorianus* (Lager) have distinct temperature ranges (18–22 °C vs. 7–15 °C) and flavor yield coefficients. 
*   **Wine vs. Beer:** Malherbe’s parameters are for **winemaking** (*S. cerevisiae* K1) in synthetic must with very high sugar ($200+ \, g/L$). Implementing these values in a beer simulator (usually $120 \, g/L$ sugar) will likely result in an overestimation of ethanol tolerance and growth rates.

### **5. Recommendation for Simulator MVP**

**Safest Version to Implement First:** **Shopska et al. (Source 2) - Monod System with Aiba Inhibition.**

**Reasons:**
1.  **Beer-Specific:** The parameters ($K_{sx}, Y_{x/s}, \mu_{max}$) were validated using a standard lager strain (*S. cerevisiae* W34/70) in 13 °P wort, which is the most common starting point for brewing simulations.
2.  **Implementation Ease:** It uses three coupled ODEs ($X, S, P$) which are standard for bioprocessing and easy to solve in Python.
3.  **Stability:** The Aiba inhibition model is more stable for simulation than quadratic models, which can become numerically unstable at very high or low substrate concentrations.
4.  **Consistency:** The units ($g/dm^3$) are easily converted to standard SI ($kg/m^3$) without the complex molar conversions required by the Ramirez/Tesema models.

**Second Step:** Layer in the **Ramirez / Maciejowski** sugar uptake logic (Priority 2) once the "engine" is running, to allow the simulator to distinguish between glucose and maltose consumption—a key requirement for professional brewing simulations.

This model specification is designed for implementation in Python using numerical integration libraries such as `scipy.integrate.solve_ivp`. It organises the extracted mathematical models into functional modules based on the sources.

### **Module 1: Primary Metabolism (The Fermentation Engine)**
*Source: Shopska et al., Yusupov et al.*

*   **State Variables:**
    *   $X$: Biomass concentration ($kg/m^3$)
    *   $S$: Substrate/Extract concentration ($kg/m^3$)
    *   $P$: Ethanol concentration ($kg/m^3$)
*   **Parameters:**
    *   $\mu_{max}$: Max specific growth rate ($s^{-1}$)
    *   $K_{sx}$: Saturation constant for growth ($kg/m^3$)
    *   $K_{ix}$: Ethanol inhibition constant for growth ($m^3/kg$)
    *   $q_{pmax}$: Max specific ethanol production rate ($s^{-1}$)
    *   $K_{sp}$: Saturation constant for product ($kg/m^3$)
    *   $Y_{x/s}, Y_{p/s}$: Yield coefficients (dimensionless $kg/kg$)
*   **ODE Right-Hand Side (RHS) Terms:**
    *   $\frac{dX}{dt} = \mu \cdot X$
    *   $\frac{dP}{dt} = q \cdot X$
    *   $\frac{dS}{dt} = -\frac{1}{Y_{x/s}} \frac{dX}{dt} - \frac{1}{Y_{p/s}} \frac{dP}{dt}$
    *   *Kinetic Expressions:* 
        *   $\mu = \mu_{max} \frac{S}{K_{sx} + S} e^{-K_{ix} P}$
        *   $q = q_{pmax} \frac{S}{K_{sp} + S}$
*   **Initial Conditions:** $X_0 = 1.0$, $P_0 = 0.0$, $S_0 = 130.0$ (standard 13 °P wort).
*   **Slider/User Inputs:** Initial Gravity ($S_0$), Pitching Rate ($X_0$).

---

### **Module 2: Secondary Metabolites (Flavor Dynamics)**
*Source: Shopska et al., Titica et al.*

*   **State Variables:**
    *   $VDK$: Vicinal Diketones / Diacetyl ($kg/m^3$)
    *   $A$: Acetaldehyde ($kg/m^3$)
    *   $E$: Esters (e.g., Ethyl Acetate) ($kg/m^3$)
    *   $FA$: Higher Alcohols (Fusel) ($kg/m^3$)
*   **Parameters:**
    *   $Y_{VDK}, Y_A, Y_E, Y_{FA}$: Growth-associated yield coefficients ($kg/kg$)
    *   $k_{VDK}, k_A$: Biomass-dependent reduction rates ($s^{-1}$)
*   **ODE RHS Terms:**
    *   $\frac{dVDK}{dt} = Y_{VDK} \cdot \mu \cdot X - k_{VDK} \cdot VDK \cdot X$
    *   $\frac{dA}{dt} = Y_A \cdot \mu \cdot X - k_A \cdot A \cdot X$
    *   $\frac{dE}{dt} = Y_E \cdot \mu \cdot X$
    *   $\frac{dFA}{dt} = Y_{FA} \cdot \mu \cdot X$
*   **Algebraic Outputs:**
    *   Total CO₂ produced ($C_p$): $C_p = (S_0 - S) \cdot Y_{CO2/S}$ (Proxy for offline sensors).
*   **Hidden Calibration Parameters:** $k_{VDK}$ and $k_A$ (highly strain-dependent).

---

### **Module 3: Thermodynamics (Heat & Temperature)**
*Source: Tesema et al.*

*   **State Variables:**
    *   $T$: Wort Temperature ($K$)
    *   $T_j$: Cooling Jacket Temperature ($K$)
*   **Parameters:**
    *   $\Delta H_{FG}$: Heat of fermentation ($J/mol$).
    *   $C_p, \rho$: Wort specific heat and density ($J/kg \cdot K, kg/m^3$).
    *   $U, A$: Overall heat transfer coefficient and area ($W/m^2 \cdot K, m^2$).
    *   $F_c$: Coolant flow rate ($m^3/s$).
    *   $T_c$: Inlet coolant temperature ($K$).
*   **ODE RHS Terms:**
    *   $\frac{dT}{dt} = \frac{-X \cdot \Delta H_{FG} \cdot \mu}{\rho \cdot C_p} - \frac{U \cdot A \cdot \Delta T_{lm}}{\rho \cdot C_p \cdot V}$
    *   $\frac{dT_j}{dt} = \frac{F_c(T_c - T_j)}{V_j} + \frac{U \cdot A \cdot \Delta T_{lm}}{\rho_c \cdot V_j \cdot C_{pc}}$
    *   $\Delta T_{lm} = (T - T_j) / \ln(T/T_j)$
*   **User Inputs:** Target Fermentation Temperature, Coolant Flow Rate ($F_c$).

---

### **Module 4: Nutrient & Amino Acid Dynamics**
*Source: Ramirez and Maciejowski via Shopska, Tesema et al.*

*   **State Variables:**
    *   $L, I, V$: Leucine, Isoleucine, Valine concentrations ($mol/m^3$).
*   **Parameters:**
    *   $Y_{LX}, Y_{IX}, Y_{VX}$: Amino acid yields per unit biomass.
    *   $\tau_D$: Time constant for uptake delay ($s$).
*   **ODE RHS Terms:**
    *   $\frac{dL}{dt} = -Y_{LX} \cdot \frac{dX}{dt} \cdot \frac{L}{K_L + L} \cdot (1 - e^{-t/\tau_D})$
*   **Initial Conditions:** $L_0, I_0, V_0$ based on specific wort FAN profile.

---

### **Module 5: Gas-Phase Losses (Stripping & Partitioning)**
*Source: Mouret et al.*

*   **Algebraic Outputs:**
    *   $C_{liq}$: Instantaneous liquid concentration.
    *   $k_i$: Partition coefficient (function of $T$ and ethanol $P$).
    *   $\ln k_i = F_1 + F_2 P - \frac{F_3 + F_4 P}{R} (\frac{1000}{T} - \frac{1000}{T_{ref}})$.
*   **ODE RHS Term (Losses):**
    *   $\frac{dL_i}{dt} = \frac{C_{liq, i}}{k_i} \cdot Q_{CO2}$
    *   Where $Q_{CO2}$ is the volumetric flow of CO₂ gas stripping the compound.

---

### **Simulation Specification Summary**

| Category | Component | Default Value (SI) | Notes |
| :--- | :--- | :--- | :--- |
| **User Inputs** | Initial Extract ($S_0$) | 130.0 $kg/m^3$ | 13 °Plato |
| | Target Temp | 288.15 $K$ | 15 °C |
| **Hidden Calibration** | $\mu_{max}$ | $6.16 \times 10^{-6} s^{-1}$ | Lager strain W34/70 |
| | $K_{sx}$ | 237.0 $kg/m^3$ | Specific to 13 °P wort |
| **Expected Plots** | **Gravity/Ethanol** | — | $S$ vs. time and $P$ vs. time |
| | **Flavor Peak** | — | Diacetyl ($VDK$) peak and tail |
| | **Temp Control** | — | Jacket $T_j$ vs. Tank $T$ |
| | **Aroma Losses** | — | Cumulative $L_i$ vs. $C_{liq}$ |

**Assumptions & Limitations:** 
*   **Laminar Flow:** Assumes no significant temperature gradients within the tank (isothermal bulk).
*   **Sugar Ordering:** Assumes a single unified substrate $S$ for MVP; for higher fidelity, implement the Ramirez sequential glucose/maltose model.