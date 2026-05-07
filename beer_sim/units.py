"""Unit conversion helpers used by process models."""


def celsius_to_kelvin(value: float) -> float:
    return value + 273.15


def hours_to_seconds(value: float) -> float:
    return value * 3600.0


def minutes_to_seconds(value: float) -> float:
    return value * 60.0


def bar_to_pascal(value: float) -> float:
    return value * 100000.0


def liters_to_cubic_meters(value: float) -> float:
    return value * 0.001


def grams_per_liter_to_kg_per_cubic_meter(value: float) -> float:
    return value


def milligrams_per_liter_to_kg_per_cubic_meter(value: float) -> float:
    return value * 0.001


def cfu_per_ml_to_cfu_per_cubic_meter(value: float) -> float:
    return value * 1.0e6
