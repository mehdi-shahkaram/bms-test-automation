# BMS Test Automation

Requirements-based test automation for a simplified Battery Management System (BMS), written in Python with pytest.

## Overview

A small Python model of a BMS for a 4-cell lithium-ion pack reads cell voltages, pack temperature and current, and decides whether charging and discharging are allowed. A pytest suite verifies every requirement, using boundary value tests at each limit.

## Requirements and traceability

| ID | Requirement | Tests |
|----|-------------|-------|
| REQ-001 | Stop charging if any cell is above 4.2 V | `test_req001_*` (2 tests) |
| REQ-002 | Stop discharging if any cell is below 3.0 V | `test_req002_*` (2 tests) |
| REQ-003 | Allow charging only between 0 °C and 45 °C | `test_req003_*` (3 tests) |
| REQ-004 | Allow discharging only between -20 °C and 60 °C | `test_req004_*` (3 tests) |
| REQ-005 | Stop discharging if current is above 100 A | `test_req005_*` (2 tests) |
| REQ-006 | Allow charging and discharging when all values are within limits | `test_req006_*` (1 test) |
| REQ-007 | Report every active fault by name | `test_req007_*` and fault checks in the tests above |

## Assumptions (version 1)

- NMC lithium-ion cells, with limits based on typical datasheet values
- Simplified behaviour: no reaction delays, no hysteresis, one temperature sensor for the whole pack
- Current sign convention: positive = discharging

## Project structure

```
bms.py              BMS logic (system under test)
tests/test_bms.py   Requirement-based test suite
pytest.ini          pytest configuration
requirements.txt    Python dependencies
```

## How to run

```
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

To generate an HTML test report:

```
pytest -v --html=report.html --self-contained-html
```

## Roadmap

- Version 2: fault reaction delays, hysteresis on recovery, more realistic behaviour
- Continuous integration with GitHub Actions
