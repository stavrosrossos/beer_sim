"""Run the default beer simulation and print a short summary."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from beer_sim import simulate
from beer_sim.config import SECONDS_PER_HOUR


def main() -> None:
    result = simulate()
    final = result.states[-1]
    summary = result.summary
    print(f"Simulated {result.time[-1] / SECONDS_PER_HOUR:.1f} hours")
    print(f"Final substrate: {final.substrate:.3f} kg/m^3")
    print(f"Final ethanol: {final.ethanol:.3f} kg/m^3")
    print(f"Final ABV: {summary.final_abv:.2f}%")
    print(f"Apparent attenuation: {summary.attenuation * 100.0:.1f}%")
    print(f"Final viable cells: {final.viable_cells:.3e} cells/m^3")
    print(f"Peak VDK proxy: {summary.peak_vdk_mg_l:.3f} mg/L")
    print(f"Final esters proxy: {summary.final_esters_mg_l:.3f} mg/L")


if __name__ == "__main__":
    main()
