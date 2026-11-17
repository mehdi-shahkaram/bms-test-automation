"""Simple Battery Management System (BMS) for a 4-cell lithium-ion pack.

Takes sensor readings and decides whether charging and discharging are allowed.
Limits are typical values for NMC lithium-ion cells (simplified, version 1).
"""

from dataclasses import dataclass, field

# Safety limits
MAX_CELL_VOLTAGE = 4.2         # V   (REQ-001)
MIN_CELL_VOLTAGE = 3.0         # V   (REQ-002)
CHARGE_TEMP_MIN = 0.0          # °C  (REQ-003)
CHARGE_TEMP_MAX = 45.0         # °C  (REQ-003)
DISCHARGE_TEMP_MIN = -20.0     # °C  (REQ-004)
DISCHARGE_TEMP_MAX = 60.0      # °C  (REQ-004)
MAX_DISCHARGE_CURRENT = 100.0  # A   (REQ-005)


@dataclass
class BmsDecision:
    """What the BMS decides. By default, everything is allowed (REQ-006)."""
    charge_allowed: bool = True
    discharge_allowed: bool = True
    faults: list = field(default_factory=list)  # REQ-007


def evaluate(cell_voltages, temperature, current):
    """Check the readings against the limits and return a BmsDecision.

    cell_voltages: list of the 4 cell voltages, in V
    temperature:   pack temperature, in °C
    current:       pack current, in A (positive = discharging)
    """
    decision = BmsDecision()

    # REQ-001: any cell above the max voltage -> stop charging
    if max(cell_voltages) > MAX_CELL_VOLTAGE:
        decision.charge_allowed = False
        decision.faults.append("OVERVOLTAGE")

    # REQ-002: any cell below the min voltage -> stop discharging
    if min(cell_voltages) < MIN_CELL_VOLTAGE:
        decision.discharge_allowed = False
        decision.faults.append("UNDERVOLTAGE")

    # REQ-003: charging only allowed between 0 and 45 °C
    if not (CHARGE_TEMP_MIN <= temperature <= CHARGE_TEMP_MAX):
        decision.charge_allowed = False
        decision.faults.append("CHARGE_TEMPERATURE")

    # REQ-004: discharging only allowed between -20 and 60 °C
    if not (DISCHARGE_TEMP_MIN <= temperature <= DISCHARGE_TEMP_MAX):
        decision.discharge_allowed = False
        decision.faults.append("DISCHARGE_TEMPERATURE")

    # REQ-005: discharge current above the max -> stop discharging
    if current > MAX_DISCHARGE_CURRENT:
        decision.discharge_allowed = False
        decision.faults.append("OVERCURRENT")

    return decision