import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

#Example test cases:
def test_calm_wind():
    assert wind_alert(10) == "none"

def test_no_alerts():
    assert overall_alert([]) == "none"

# Wind alert: both outcomes of every threshold, including boundaries
def test_wind_warning():
    assert wind_alert(100) == "warning"

def test_wind_warning_boundary():
    assert wind_alert(89) == "warning"

def test_wind_watch():
    assert wind_alert(70) == "watch"

def test_wind_watch_boundary():
    assert wind_alert(62) == "watch"

def test_wind_advisory():
    assert wind_alert(45) == "advisory"

def test_wind_advisory_boundary():
    assert wind_alert(39) == "advisory"

def test_wind_just_below_advisory():
    assert wind_alert(38) == "none"

# Rain alert: every combination of rain level and soil saturation
def test_heavy_rain_saturated_soil():
    assert rain_alert(60, True) == "warning"

def test_heavy_rain_dry_soil():
    assert rain_alert(60, False) == "watch"

def test_heavy_rain_boundary():
    assert rain_alert(50, True) == "warning"

def test_moderate_rain_saturated_soil():
    assert rain_alert(20, True) == "watch"

def test_moderate_rain_dry_soil():
    assert rain_alert(20, False) == "advisory"

def test_moderate_rain_boundary():
    assert rain_alert(10, False) == "advisory"

def test_light_rain():
    assert rain_alert(5, False) == "none"

def test_light_rain_saturated_soil():
    assert rain_alert(9, True) == "none"

# Heat alert: humidity above and at/below 40, every index level
def test_heat_warning():
    assert heat_alert(44, 60) == "warning"

def test_heat_watch():
    assert heat_alert(39, 60) == "watch"

def test_heat_advisory():
    assert heat_alert(34, 60) == "advisory"

def test_heat_none():
    assert heat_alert(25, 60) == "none"

def test_heat_low_humidity_no_adjustment():
    assert heat_alert(44, 30) == "watch"

def test_heat_humidity_boundary_no_adjustment():
    assert heat_alert(34, 40) == "none"

def test_heat_warning_boundary_low_humidity():
    assert heat_alert(45, 20) == "warning"

def test_heat_advisory_boundary_low_humidity():
    assert heat_alert(35, 20) == "advisory"

# Overall alert: worse, not worse, and unknown alerts
def test_overall_picks_worst():
    assert overall_alert(["advisory", "warning", "watch"]) == "warning"

def test_overall_all_none():
    assert overall_alert(["none", "none"]) == "none"

def test_overall_same_severity_keeps_worst():
    assert overall_alert(["watch", "watch"]) == "watch"

def test_overall_single_alert():
    assert overall_alert(["advisory"]) == "advisory"

def test_overall_unknown_alert():
    with pytest.raises(ValueError):
        overall_alert(["storm"])

def test_overall_unknown_after_valid():
    with pytest.raises(ValueError):
        overall_alert(["warning", "hurricane"])
