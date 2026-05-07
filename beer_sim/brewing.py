"""Brewing gravity, extract, attenuation, and ABV calculations."""

from __future__ import annotations


FERMENTABLE_POTENTIALS_PPG = {
    "Dry malt extract (DME)": 44.0,
    "Liquid malt extract (LME)": 36.0,
    "Base grain": 37.0,
}


def gravity_points_from_sg(specific_gravity: float) -> float:
    """Return gravity points from specific gravity."""

    if specific_gravity < 1.0:
        raise ValueError("specific_gravity must be at least 1.000")
    return (specific_gravity - 1.0) * 1000.0


def sg_from_gravity_points(points: float) -> float:
    """Return specific gravity from gravity points."""

    return 1.0 + max(points, 0.0) / 1000.0


def recipe_gravity_points(
    fermentable_weight_lb: float,
    potential_ppg: float,
    batch_volume_gal: float,
    efficiency: float = 1.0,
) -> float:
    """Return predicted gravity points from lb, PPG, gallons, and efficiency."""

    if batch_volume_gal <= 0.0:
        raise ValueError("batch_volume_gal must be positive")
    if fermentable_weight_lb < 0.0:
        raise ValueError("fermentable_weight_lb must be non-negative")
    if potential_ppg < 0.0:
        raise ValueError("potential_ppg must be non-negative")
    if efficiency < 0.0:
        raise ValueError("efficiency must be non-negative")
    return fermentable_weight_lb * potential_ppg * efficiency / batch_volume_gal


def sg_from_recipe(
    fermentable_weight_lb: float,
    potential_ppg: float,
    batch_volume_gal: float,
    efficiency: float = 1.0,
) -> float:
    """Return predicted OG from extract or grain potential."""

    return sg_from_gravity_points(
        recipe_gravity_points(fermentable_weight_lb, potential_ppg, batch_volume_gal, efficiency)
    )


def dilute_gravity_points(points_1: float, volume_1: float, volume_2: float) -> float:
    """Return gravity points after dilution or boil-off using points * volume conservation."""

    if volume_2 <= 0.0:
        raise ValueError("volume_2 must be positive")
    if volume_1 < 0.0:
        raise ValueError("volume_1 must be non-negative")
    return max(points_1, 0.0) * volume_1 / volume_2


def plato_from_sg(specific_gravity: float) -> float:
    """Return degrees Plato from specific gravity using a common cubic approximation."""

    sg = specific_gravity
    return -616.868 + 1111.14 * sg - 630.272 * sg**2 + 135.997 * sg**3


def sg_from_plato(plato: float) -> float:
    """Return specific gravity from degrees Plato using a common brewing approximation."""

    plato = max(plato, 0.0)
    return 1.0 + plato / (258.6 - ((plato / 258.2) * 227.1))


def extract_g_l_from_sg(specific_gravity: float) -> float:
    """Approximate extract in g/L from SG via Plato * 10."""

    return max(plato_from_sg(specific_gravity), 0.0) * 10.0


def sg_from_extract_g_l(extract_g_l: float) -> float:
    """Approximate SG from extract in g/L via Plato."""

    return sg_from_plato(max(extract_g_l, 0.0) / 10.0)


def abv_from_gravity(original_gravity: float, final_gravity: float) -> float:
    """Return brewing-style ABV estimate from OG and FG."""

    return max((original_gravity - final_gravity) * 131.25, 0.0)


def apparent_attenuation_from_gravity(original_gravity: float, final_gravity: float) -> float:
    """Return apparent attenuation fraction from OG and FG."""

    denominator = original_gravity - 1.0
    if denominator <= 0.0:
        return 0.0
    return max(min((original_gravity - final_gravity) / denominator, 1.0), 0.0)


def estimate_final_gravity_from_og(original_gravity: float, remaining_points_fraction: float = 0.25) -> float:
    """Estimate FG by retaining a fraction of original gravity points."""

    points = gravity_points_from_sg(original_gravity)
    return sg_from_gravity_points(points * remaining_points_fraction)
