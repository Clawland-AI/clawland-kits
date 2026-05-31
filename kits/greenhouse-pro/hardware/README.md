# Greenhouse Pro Hardware Sources

This directory contains the reviewable schematic source for the Greenhouse Pro
kit.

## Files

- `greenhouse-pro.kicad_sch` - KiCad schematic source for the PicClaw edge
  board connectors, I2C sensor bus, soil-probe analog inputs, DS18B20 pull-up,
  and relay-control outputs.

## Review Notes

- The schematic is intentionally connector-level because the kit uses modular
  breakout boards from the BOM rather than a custom PCB.
- Relay load wiring is documented in `../WIRING.md` and should remain isolated
  from the low-voltage enclosure.
- Sensor addresses and calibration expectations are documented in
  `../test-report.md`.
