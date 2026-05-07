import pytest

from beer_sim.brewing import (
    abv_from_gravity,
    apparent_attenuation_from_gravity,
    dilute_gravity_points,
    estimate_final_gravity_from_og,
    extract_g_l_from_sg,
    gravity_points_from_sg,
    recipe_gravity_points,
    sg_from_extract_g_l,
    sg_from_gravity_points,
    sg_from_recipe,
)


def test_dme_one_lb_one_gallon_yields_1044():
    assert recipe_gravity_points(1.0, 44.0, 1.0) == pytest.approx(44.0)
    assert sg_from_recipe(1.0, 44.0, 1.0) == pytest.approx(1.044)


def test_abv_from_gravity():
    assert abv_from_gravity(1.050, 1.010) == pytest.approx(5.25)


def test_apparent_attenuation_from_gravity():
    assert apparent_attenuation_from_gravity(1.050, 1.010) == pytest.approx(0.80)


def test_gravity_points_round_trip():
    assert gravity_points_from_sg(1.050) == pytest.approx(50.0)
    assert sg_from_gravity_points(50.0) == pytest.approx(1.050)


def test_dilution_conserves_gravity_points():
    assert dilute_gravity_points(60.0, 5.0, 6.0) == pytest.approx(50.0)


def test_extract_sg_round_trip_is_close():
    extract = extract_g_l_from_sg(1.048)
    assert sg_from_extract_g_l(extract) == pytest.approx(1.048, abs=0.001)


def test_estimate_final_gravity_retains_25_percent_of_points():
    assert estimate_final_gravity_from_og(1.050) == pytest.approx(1.0125)
