The core equations across the sources describe the physical and biochemical phenomena of oxygen mass transfer, microbial growth, and the brewing process. The following table provides these equations with variables converted to **consistent SI units** (kilograms, meters, seconds, Kelvin, and Pascals).

### Core Equations in Bioprocessing and Brewing

| Process Category | Core Equation | Variable Definitions (SI Units) | Source |
| :--- | :--- | :--- | :--- |
| **Oxygen Mass Transfer** | $OTR = k_La (C^* - C)$ | $OTR$: Oxygen Transfer Rate ($kg \cdot m^{-3}s^{-1}$); $k_La$: Volumetric mass transfer coefficient ($s^{-1}$); $C^*, C$: Saturated and actual dissolved oxygen ($kg \cdot m^{-3}$). | |
| **Power Input (Aerated)** | $P_g = c ( \frac{P_{g0} N D_i^3}{F_g^{0.56}} )^{-0.45}$ | $P_g$: Aerated power ($W$); $P_{g0}$: Non-aerated power ($W$); $N$: Agitation rate ($s^{-1}$); $D_i$: Impeller diameter ($m$); $F_g$: Gas flow rate ($m^3s^{-1}$). | |
| **Microbial Growth (FOPDT)** | $T_L \frac{dx_1}{dt} + x_1 = x_{1,max}(t - t_L)$ | $x_1$: Total cell concentration ($cells \cdot m^{-3}$); $T_L$: Time constant ($s$); $t_L$: Lag time ($s$). | |
| **Viable Cell Dynamics** | $x_v = x_1 - x_2$ | $x_v, x_1, x_2$: Viable, total, and dead cell concentrations ($cells \cdot m^{-3}$). | |
| **Product Formation** | $\frac{dP}{dt} = Y_{P/X} \frac{dx_v}{dt} + m_P x_v$ | $P$: Ethanol concentration ($kg \cdot m^{-3}$); $Y_{P/X}$: Yield coefficient ($kg \cdot cell^{-1}$); $m_P$: Maintenance coefficient ($kg \cdot cell^{-1}s^{-1}$). | |
| **Specific Growth Rate** | $\mu = \mu_{max} \frac{S}{K_s + S}$ | $\mu$: Specific growth rate ($s^{-1}$); $S$: Substrate concentration ($kg \cdot m^{-3}$); $K_s$: Saturation constant ($kg \cdot m^{-3}$). | |
| **Sugar Consumption (Substrate Depletion)** | $\frac{dC_S}{dt} = -\mu_S \cdot X_A$ | $C_S$: Sugar/substrate concentration ($kg \cdot m^{-3}$); $\mu_S$: Specific substrate consumption rate ($kg \cdot cell^{-1}s^{-1}$); $X_A$: Active yeast biomass ($cells \cdot m^{-3}$). | |
| **Reaction Kinetics (Arrhenius)** | $k = k_0 \exp( \frac{-E_a}{RT} )$ | $k$: Reaction rate constant; $E_a$: Activation energy ($J \cdot mol^{-1}$); $R$: Gas constant ($8.314 J \cdot mol^{-1}K^{-1}$); $T$: Temperature ($K$). | |
| **Lautering (Darcy's Law)** | $Q = \frac{\pi p r^4 t s z}{8 \eta l}$ | $Q$: Filtered volume ($m^3$); $p$: Pressure difference ($Pa$); $\eta$: Dynamic viscosity ($Pa \cdot s$); $l$: Bed length ($m$). | |
| **Heat Transfer (Fourier)** | $q = \frac{K_a A \Delta T}{X}$ | $q$: Heat transfer rate ($W$); $K_a$: Thermal conductivity ($W \cdot m^{-1}K^{-1}$); $A$: Area ($m^2$); $X$: Wall thickness ($m$). | |
| **Wort Flavor Degradation** | $-\frac{dC_A}{dt} = k C_A^n$ | $C_A$: Concentration of flavour compound ($kg \cdot m^{-3}$); $n$: Reaction order. | |

### Important Unit Conversions Used
To maintain consistency with the SI standard, the following conversions from the sources' original units were applied:
*   **Pressure:** 1 bar = $10^5$ Pascals ($Pa$).
*   **Time:** 1 hour = 3,600 seconds ($s$); 1 minute = 60 seconds.
*   **Mass/Concentration:** 1 mg/L = $0.001 kg/m^3$; 1 g/L = $1 kg/m^3$.
*   **Temperature:** $T(K) = T(^\circ C) + 273.15$.
*   **Volume:** 1 mL = $10^{-6} m^3$; 1 L = $10^{-3} m^3$.
*   **Cell Counts:** CFU/mL was converted to $10^6$ CFU/$m^3$.

Based on the sources provided, the typical values for the maximum growth rate ($\mu_{max}$) and the half-saturation constant ($K_s$) for standard Brewer's Yeast are described as follows:

### **Maximum Growth Rate ($\mu_{max}$)**
The sources provide a specific growth rate value for an autochthonous yeast strain, ***Saccharomyces cerevisiae* PB101**, which was studied for its probiotic potential in beer production. 
*   **Value:** In a logistic growth model, the specific growth rate ($\mu_1$) for this strain is listed as **0.2**. 
*   **Context:** This parameter is defined as the **maximum rate at which yeast biomass increases**, which is dependent on substrate availability and environmental conditions. 
*   **Comparison:** While the sources use a standard commercial yeast (Safale US05) as a control, they primarily focus on the kinetic modeling of the PB101 strain, noting that the autochthonous yeast generally exhibits lower sugar consumption and alcohol production compared to the commercial "standard" strain.

### **Half-Saturation Constant ($K_s$)**
The sources discuss the mathematical definition of $K_s$ (also referred to as $K_{sx}$) within the context of the Monod equation and its variants used to describe fermentation kinetics.
*   **Definition:** $K_s$ is defined as the **saturation constant**, with units typically expressed in **$g/dm^3$**.
*   **Numerical Value:** The provided excerpts **do not list a specific "typical" numerical value** for $K_s$ for standard Brewer's Yeast. Instead, they emphasize that these constants must be identified experimentally or through optimization for specific fermentation conditions. 

### **Other Related Kinetic Parameters**
For the probiotic brewing strain PB101, the sources also identify several other critical growth parameters:
*   **Time Constant ($T_L$):** 7 hours (the time required to reach 63.2% of maximum population change).
*   **Lag Time ($t_L$):** 24 hours (the delay before active growth begins).
*   **Maximum Total Cell Population ($X_{1,max}$):** $1.28 \times 10^8$ CFU/mL.
*   **Death Rate ($\mu_2$):** 0.092, representing the rate at which cells transition from viable to dead.

The sources do not provide a single, definitive temperature range for yeast death or dormancy across all strains. Instead, they specify different temperature thresholds for **growth, survival, and sterilization** depending on the yeast type and the specific process being modeled.

### **Growth and Active Fermentation Ranges**
Standard brewing yeast growth is typically divided by fermentation style:
*   **Top-fermenting (Ale) strains:** These carry out the fermentation process at temperatures between **15 °C and 25 °C**.
*   **Bottom-fermenting (Lager) strains:** These operate in a lower temperature range, between **8 °C and 15 °C**.
*   **Probiotic Tolerance:** Some specific strains, such as *Saccharomyces cerevisiae* PB101, exhibit a high tolerance to heat, showing active growth at **37 °C, 39 °C, and 42 °C**.

### **Dormancy and Cold Storage**
While the sources do not explicitly use the term "dormancy," they describe conditions where yeast remains viable but at significantly reduced activity:
*   **Maturation:** Finished beer is often subjected to cold maturation at **4 °C**. 
*   **Viability:** Research on probiotic beer indicates that yeast can remain viable for at least **60 days** when stored at these cold temperatures.

### **Lethal and Sterilization Temperatures**
Temperatures used in the earlier stages of brewing are designed to be lethal to microorganisms to ensure a sterile environment for the pitched yeast:
*   **Sterilization:** The boiling of wort (typically at **100 °C** at atmospheric pressure) is explicitly performed for the **sterilization of the wort**. 
*   **Enzyme Inactivation:** During the mashing and lautering processes, temperatures are maintained between **75 °C and 78 °C**. At temperatures above **80 °C**, critical enzymes like $\alpha$-amylase are inactivated, and this environment is generally unsuitable for yeast survival.
*   **Gastrointestinal Survival:** In simulated human digestion at **37 °C**, a reduction in survival of approximately **20–28%** was observed for the PB101 strain, indicating that while the yeast is tolerant, body temperature and environmental factors (like pH and bile salts) begin to compromise the population.

