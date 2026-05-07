from beer_sim.models.fermentation import sugar_consumption_rate
from beer_sim.models.growth import cardinal_temperature_factor, monod_specific_growth_rate, viable_cells
from beer_sim.models.oxygen import oxygen_consumption_rate, oxygen_transfer_rate
import pytest


def test_oxygen_transfer_rate_uses_concentration_gradient():
    assert oxygen_transfer_rate(0.5, 8.0, 2.0) == 3.0


def test_monod_growth_rate_is_zero_without_substrate():
    assert monod_specific_growth_rate(mu_max=1.0, substrate=0.0, ks=1.0) == 0.0


def test_monod_growth_rate_approaches_mu_max():
    assert monod_specific_growth_rate(mu_max=1.0, substrate=99.0, ks=1.0) == 0.99


def test_viable_cells_do_not_go_negative():
    assert viable_cells(total_cells=1.0, dead_cells=2.0) == 0.0


def test_sugar_consumption_rate_is_negative():
    assert sugar_consumption_rate(2.0, 3.0) == -6.0


def test_cardinal_temperature_factor_peaks_at_optimum():
    assert cardinal_temperature_factor(30.0, 3.0, 30.0, 41.0) == pytest.approx(1.0)


def test_cardinal_temperature_factor_is_zero_outside_range():
    assert cardinal_temperature_factor(42.0, 3.0, 30.0, 41.0) == 0.0


def test_oxygen_consumption_rate_requires_biomass_and_oxygen():
    assert oxygen_consumption_rate(1.0, 0.0, 1.0, 1.0) == 0.0
    assert oxygen_consumption_rate(1.0, 1.0, 0.0, 1.0) == 0.0
