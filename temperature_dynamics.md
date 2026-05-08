Based on the provided sources, the mathematical equations governing heat transfer, cooling, and metabolic heat generation are as follows:

### 1. Fermentation Tank Energy Balance
This equation describes the rate of temperature change in the wort due to metabolic heat production and cooling.
*   **Exact Equation:** $\frac{dT}{dt} = \frac{-X \cdot \Delta H_{FG} \cdot \mu_1}{\rho \cdot C_p} - \frac{U \cdot A \cdot \Delta T_{lm}}{\rho \cdot C_p \cdot V}$
*   **State Variables:** $T$ (Wort temperature, $^\circ C$).
*   **Parameters and Units:**
    *   $X$: Biomass concentration ($mol \cdot m^{-3}$).
    *   $\Delta H_{FG}$: Overall heat of formation for glucose ($kJ \cdot mol^{-1}$).
    *   $\mu_1$: Specific rate of glucose uptake ($h^{-1}$).
    *   $\rho$: Wort density ($kg \cdot m^{-3}$).
    *   $C_p$: Specific heat capacity of wort ($kJ \cdot kg^{-1} \cdot ^\circ C^{-1}$).
    *   $U$: Heat transfer coefficient ($W \cdot m^{-2} \cdot ^\circ C^{-1}$).
    *   $A$: Heat transfer area ($m^2$).
    *   $\Delta T_{lm}$: Log-mean temperature difference between tank and jacket, defined as $\frac{T - T_j}{\ln(T/T_j)}$.
    *   $V$: Volume of fermentation tank ($m^3$).
*   **Default Values:** $\Delta H_{FG} = 17.5 \, kJ/mol$; $\rho = 1053 \, kg/m^3$; $C_p = 4.18 \, kJ/(kg \cdot ^\circ C)$.
*   **Tank Volume and Geometry:** Cylindroconical fermentation tank. Simulations used 2D axial symmetry.
*   **Coolant Flow Rates:** Evaluated at **1.2, 1.3, 1.4 (standard baseline), and 1.6 $m^3/hr$**.
*   **Heat Transfer Coefficient ($U$):** Not explicitly given as a single numeric constant, but identified as a variable dependent on geometry and conditions in $W/m^2 \cdot ^\circ C$.
*   **Heat Generation Basis:** Based on **sugar consumption** (specifically the specific uptake rate of glucose, $\mu_1$).
*   **Source:** Source 6 (Tesema et al.), p. 6, Eq. (1).
*   **Assumptions and Limitations:** Cooling jacket is perfectly insulated (no loss to surroundings); $C_p$ and $\rho$ remain constant; wort is a homogeneous liquid; flow is laminar.

### 2. Cooling Jacket Energy Balance
This equation models the temperature dynamics within the jacket as coolant circulates.
*   **Exact Equation:** $\frac{dT_j}{dt} = \frac{F_c(T_c - T_j)}{V_j} + \frac{U \cdot A \cdot \Delta T_{lm}}{\rho_c \cdot V_j \cdot C_{pc}}$
*   **State Variables:** $T_j$ (Cooling jacket temperature, $^\circ C$).
*   **Parameters and Units:**
    *   $F_c$: Coolant flow rate ($m^3 \cdot h^{-1}$).
    *   $T_c$: Coolant inlet temperature ($^\circ C$).
    *   $V_j$: Volume of the cooling jacket ($m^3$).
    *   $\rho_c$: Density of coolant ($kg \cdot m^{-3}$).
    *   $C_{pc}$: Specific heat capacity of coolant ($kJ \cdot kg^{-1} \cdot ^\circ C^{-1}$).
*   **Default Values:** Coolant used is typically **liquid circulated ammonia**. Flow rates ranged from 1.2 to 1.6 $m^3/h$.
*   **Source:** Source 6 (Tesema et al.), p. 6, Eq. (2).
*   **Assumptions and Limitations:** Assumes energy accumulation equals energy in minus energy out plus heat absorbed from the tank.

### 3. Distributed Conduction-Convection Model
Used for finite element modeling of spatial temperature profiles.
*   **Exact Equation:** $\rho C_p \left( u \frac{\partial T}{\partial x} + v \frac{\partial T}{\partial y} \right) = k \left( \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} \right)$
*   **State Variables:** $T$ (Temperature, $^\circ C$); $u, v$ (Fluid velocity components, $m/s$).
*   **Parameters and Units:** $k$ (Thermal conductivity of wort).
*   **Geometry:** Cylindroconical tank with mixing direction from upper to lower.
*   **Source:** Source 6 (Tesema et al.), Section 2, Eq. (3).
*   **Assumptions and Limitations:** Uses incompressible Navier-Stokes equations and continuity equations for laminar flow.

### 4. Wort Boiling Heat Transfer
*   **Exact Equation:** $q = \frac{K_a A \Delta T}{X}$
*   **State Variables:** $q$ (Heat transfer rate).
*   **Parameters and Units:**
    *   $K_a$: Coefficient of thermal conductivity of the kettle material.
    *   $A$: Cross-section area of heat exchange.
    *   $\Delta T$: Average temperature difference between steam and heated liquid.
    *   $X$: Wall thickness.
*   **Stage Applied:** Wort boiling.
*   **Source:** Source 12 (Shopska et al. review), p. 12, Eq. (15).
*   **Assumptions and Limitations:** A fine film of water vapor forms on the heating surface during intense boiling, which reduces heat transfer efficiency.

### 5. Temperature-Dependent Reaction Kinetics (Arrhenius)
Describes how the biological and chemical rates ($k, \mu$) vary with absolute temperature.
*   **Exact Equation:** $\mu_i = \mu_{i0} \exp\left( \frac{-E_a}{RT} \right)$
*   **State Variables:** $\mu_i$ (Specific rate of sugar uptake or biomass growth, $h^{-1}$).
*   **Parameters and Units:**
    *   $\mu_{i0}$: Arrhenius frequency factor ($h^{-1}$).
    *   $E_a$: Activation energy ($cal \cdot mol^{-1}$ or $J \cdot mol^{-1}$).
    *   $R$: Gas constant ($1.987 \, cal \cdot mol^{-1} \cdot K^{-1}$ or $8.314 \, J \cdot mol^{-1} \cdot K^{-1}$).
    *   $T$: Absolute temperature ($K$).
*   **Default Values (Frequency Factors in $\ln(h^{-1})$):** Glucose ($\ln \mu_{G0}$) = 35.77; Maltose ($\ln \mu_{M0}$) = 16.4; Maltotriose ($\ln \mu_{N0}$) = 10.59.
*   **Source:** Source 2 (Shopska et al.), Table 13.2; Source 12, Eq. (28).
*   **Assumptions and Limitations:** This part of kinetics is valid for the utilization of the three major sugars (glucose, maltose, maltotriose) in wort.