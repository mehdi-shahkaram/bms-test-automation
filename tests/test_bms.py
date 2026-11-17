"""Requirement-based tests for the BMS (version 1).

Each test name starts with the requirement it verifies.
"""

from bms import evaluate

# Normal, safe readings. Each test changes only the one value it is testing.
NORMAL_CELLS = [3.7, 3.7, 3.7, 3.7]  # V
NORMAL_TEMP = 25.0                   # °C
NORMAL_CURRENT = 10.0                # A (discharging)


# REQ-006: normal operation
def test_req006_normal_readings_allow_everything():
    result = evaluate(NORMAL_CELLS, NORMAL_TEMP, NORMAL_CURRENT)
    assert result.charge_allowed
    assert result.discharge_allowed
    assert result.faults == []


# REQ-001: overvoltage
def test_req001_voltage_at_limit_allows_charging():
    result = evaluate([4.2, 3.7, 3.7, 3.7], NORMAL_TEMP, NORMAL_CURRENT)
    assert result.charge_allowed


def test_req001_overvoltage_blocks_charging():
    result = evaluate([4.21, 3.7, 3.7, 3.7], NORMAL_TEMP, NORMAL_CURRENT)
    assert not result.charge_allowed
    assert result.discharge_allowed
    assert "OVERVOLTAGE" in result.faults


# REQ-002: undervoltage
def test_req002_voltage_at_limit_allows_discharging():
    result = evaluate([3.0, 3.7, 3.7, 3.7], NORMAL_TEMP, NORMAL_CURRENT)
    assert result.discharge_allowed


def test_req002_undervoltage_blocks_discharging():
    result = evaluate([2.99, 3.7, 3.7, 3.7], NORMAL_TEMP, NORMAL_CURRENT)
    assert not result.discharge_allowed
    assert result.charge_allowed
    assert "UNDERVOLTAGE" in result.faults


# REQ-003: charging temperature window (0 to 45 °C)
def test_req003_charging_allowed_at_both_limits():
    assert evaluate(NORMAL_CELLS, 0.0, NORMAL_CURRENT).charge_allowed
    assert evaluate(NORMAL_CELLS, 45.0, NORMAL_CURRENT).charge_allowed


def test_req003_charging_blocked_below_zero():
    result = evaluate(NORMAL_CELLS, -0.1, NORMAL_CURRENT)
    assert not result.charge_allowed
    assert result.discharge_allowed
    assert "CHARGE_TEMPERATURE" in result.faults


def test_req003_charging_blocked_above_45():
    result = evaluate(NORMAL_CELLS, 45.1, NORMAL_CURRENT)
    assert not result.charge_allowed
    assert result.discharge_allowed
    assert "CHARGE_TEMPERATURE" in result.faults


# REQ-004: discharging temperature window (-20 to 60 °C)
def test_req004_discharging_allowed_at_both_limits():
    assert evaluate(NORMAL_CELLS, -20.0, NORMAL_CURRENT).discharge_allowed
    assert evaluate(NORMAL_CELLS, 60.0, NORMAL_CURRENT).discharge_allowed


def test_req004_discharging_blocked_below_minus_20():
    result = evaluate(NORMAL_CELLS, -20.1, NORMAL_CURRENT)
    assert not result.discharge_allowed
    assert "DISCHARGE_TEMPERATURE" in result.faults


def test_req004_discharging_blocked_above_60():
    result = evaluate(NORMAL_CELLS, 60.1, NORMAL_CURRENT)
    assert not result.discharge_allowed
    assert "DISCHARGE_TEMPERATURE" in result.faults


# REQ-005: overcurrent
def test_req005_current_at_limit_allows_discharging():
    result = evaluate(NORMAL_CELLS, NORMAL_TEMP, 100.0)
    assert result.discharge_allowed


def test_req005_overcurrent_blocks_discharging():
    result = evaluate(NORMAL_CELLS, NORMAL_TEMP, 100.1)
    assert not result.discharge_allowed
    assert result.charge_allowed
    assert "OVERCURRENT" in result.faults


# REQ-007: every active fault is reported
def test_req007_multiple_faults_are_all_reported():
    result = evaluate(NORMAL_CELLS, 65.0, NORMAL_CURRENT)
    assert "CHARGE_TEMPERATURE" in result.faults
    assert "DISCHARGE_TEMPERATURE" in result.faults