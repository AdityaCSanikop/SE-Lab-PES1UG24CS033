import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

#Example test cases:
def test_calm_wind():
    assert wind_alert(10) == "none"

def test_no_alerts():
    assert overall_alert([]) == "none"

# Wind alert levels
def test_wind_warning():
    assert wind_alert(100) == "warning"

def test_wind_watch():
    assert wind_alert(70) == "watch"

def test_wind_advisory():
    assert wind_alert(45) == "advisory"

# Rain alert levels
def test_heavy_rain_saturated_soil():
    assert rain_alert(60, True) == "warning"

def test_heavy_rain_dry_soil():
    assert rain_alert(60, False) == "watch"

def test_moderate_rain_saturated_soil():
    assert rain_alert(20, True) == "watch"

def test_moderate_rain_dry_soil():
    assert rain_alert(20, False) == "advisory"

def test_light_rain():
    assert rain_alert(5, False) == "none"

# Heat alert levels (humidity > 40 adds to the heat index)
def test_heat_warning():
    assert heat_alert(44, 60) == "warning"

def test_heat_watch():
    assert heat_alert(39, 60) == "watch"

def test_heat_advisory():
    assert heat_alert(34, 60) == "advisory"

def test_heat_none():
    assert heat_alert(25, 60) == "none"

# Overall alert
def test_overall_picks_worst():
    assert overall_alert(["advisory", "warning", "watch"]) == "warning"

def test_overall_unknown_alert():
    with pytest.raises(ValueError):
        overall_alert(["storm"])
