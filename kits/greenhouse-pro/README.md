# Greenhouse Pro Kit

Greenhouse Pro is a low-cost Clawland hardware kit for unattended greenhouse monitoring. It combines climate, soil, light, and carbon-dioxide signals with PicClaw alert rules so an operator can catch irrigation, ventilation, and heating issues before crops are stressed.

## Use Case

The kit is designed for a small greenhouse bay or high-value grow tent where a human attendant would normally make regular rounds to check soil moisture, canopy temperature, humidity, ventilation, and light exposure.

Target replacement value from the Clawland bounty board:

| Scenario | Cost |
| --- | ---: |
| Greenhouse attendant rounds | USD 18,000 per year |
| Greenhouse Pro kit | about USD 116 one time |
| First-year savings estimate | about USD 17,884 |

## What Is Included

- Complete Bill of Materials in `BOM.md`.
- ASCII wiring guide and assembly steps in `WIRING.md`.
- KiCad schematic source in `hardware/greenhouse-pro.kicad_sch`.
- PicClaw skill configuration in `skill.yaml`.
- Alert and escalation thresholds in `alerts.yaml`.
- Sensor driver stubs in `drivers/`.
- 3D-printable enclosure source in `enclosure/greenhouse-pro-enclosure.scad`.
- Grafana dashboard template in `dashboard.json`.
- Test and calibration report in `test-report.md`.
- Dependency-free validator in `scripts/validate_greenhouse_pro.py`.

## Sensors And Actuators

| Signal | Part | Purpose |
| --- | --- | --- |
| Air temperature and humidity | BME280 | Canopy climate and dew-point risk |
| Soil moisture | Capacitive soil probe | Irrigation deficit and overwatering checks |
| Light intensity | BH1750 | Daily light integral approximation |
| Carbon dioxide | SCD41 | Ventilation and photosynthesis signal |
| Leaf surface temperature | DS18B20 probe | Heat stress and HVAC lag detection |
| Relay output | 2-channel relay board | Fan and irrigation pump control |

## Operating Profile

The PicClaw node samples every 60 seconds, publishes telemetry to the Clawland edge bus, and evaluates local guardrails:

- Fan boost when temperature or CO2 crosses warning thresholds.
- Pump lockout when soil moisture is already high.
- Critical alert when heat stress, low humidity, or sensor staleness persists.
- Daily report containing min, max, average, and threshold excursion counts.

## Quick Start

1. Order the parts from `BOM.md`.
2. Wire the kit using `WIRING.md`.
3. Review the KiCad schematic in `hardware/greenhouse-pro.kicad_sch`.
4. Print the enclosure from `enclosure/greenhouse-pro-enclosure.scad`.
5. Import `dashboard.json` into Grafana if the site exports Prometheus-style telemetry.
6. Copy `skill.yaml` and `alerts.yaml` to the PicClaw skill directory.
7. Flash the driver scripts from `drivers/` onto the node.
8. Run the validation script:

```bash
python kits/greenhouse-pro/scripts/validate_greenhouse_pro.py
```

9. Calibrate the soil probe using the dry and saturated readings in `test-report.md`.

## Safety Notes

- Keep mains-powered fans and pumps isolated from the low-voltage sensor enclosure.
- Use a relay module with opto-isolation and a fused load circuit.
- Do not mount the controller where condensation can drip into the enclosure.
- Treat CO2 readings as a ventilation signal only; this kit is not a life-safety monitor.
