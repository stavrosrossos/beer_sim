from beer_sim.units import (
    bar_to_pascal,
    celsius_to_kelvin,
    cfu_per_ml_to_cfu_per_cubic_meter,
    grams_per_liter_to_kg_per_cubic_meter,
    hours_to_seconds,
    liters_to_cubic_meters,
    milligrams_per_liter_to_kg_per_cubic_meter,
    minutes_to_seconds,
)


def test_spec_unit_conversions():
    assert bar_to_pascal(1.0) == 100000.0
    assert hours_to_seconds(1.0) == 3600.0
    assert minutes_to_seconds(1.0) == 60.0
    assert celsius_to_kelvin(20.0) == 293.15
    assert liters_to_cubic_meters(1.0) == 0.001
    assert grams_per_liter_to_kg_per_cubic_meter(1.0) == 1.0
    assert milligrams_per_liter_to_kg_per_cubic_meter(1.0) == 0.001
    assert cfu_per_ml_to_cfu_per_cubic_meter(1.0) == 1.0e6
