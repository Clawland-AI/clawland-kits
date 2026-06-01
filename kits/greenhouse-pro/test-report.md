# Greenhouse Pro Test Report

This report documents the validation procedure and a representative calibration dataset for the Greenhouse Pro kit. The sample readings are bench data intended to verify configuration, thresholds, and report formatting before installation with live plants.

## Calibration Procedure

1. Power the controller from a 5 V supply and confirm sensor discovery.
2. Read the BME280, BH1750, and SCD41 for five minutes in ambient air.
3. Calibrate each capacitive soil probe:
   - dry reading: probe in air for 30 seconds;
   - wet reading: probe in saturated potting media for 60 seconds;
   - store both ADC values in `skill.yaml`.
4. Heat-test the BME280 by raising ambient temperature near the sensor shield by 4 C.
5. Shade-test BH1750 by covering the diffuser for 20 seconds.
6. Relay-test fan and pump outputs with no load, then with fused greenhouse loads.

## Sample Readings

| Time | Air C | RH % | CO2 ppm | Lux | Soil A % | Soil B % | Leaf C | Expected rule |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 08:00 | 22.4 | 66 | 610 | 18400 | 54 | 51 | 21.9 | none |
| 12:00 | 31.8 | 72 | 1220 | 51200 | 42 | 39 | 31.2 | none |
| 14:15 | 33.1 | 76 | 1580 | 48800 | 34 | 32 | 32.8 | high_canopy_temperature, ventilation_needed |
| 16:20 | 29.3 | 81 | 1010 | 21000 | 27 | 26 | 28.7 | low_soil_moisture |
| 18:00 | 24.8 | 89 | 760 | 6400 | 74 | 71 | 24.2 | ventilation_needed |

## Pass Criteria

- All configured sensors appear in the daily report.
- Warning and critical thresholds map to the expected rules.
- Pump action never runs when either soil probe is above 82 percent.
- Fan action runs for high temperature, high humidity, or high CO2.
- Relay dry-run toggles log events before physical loads are attached.

## Known Assumptions

- Actual greenhouse setpoints differ by crop. Tomatoes tolerate warmer days than leafy greens.
- CO2 enrichment workflows must obey local safety guidance.
- The kit is not a pesticide, fertigation, or life-safety controller.
- Sensor placement affects readings; perform final calibration after installation.

