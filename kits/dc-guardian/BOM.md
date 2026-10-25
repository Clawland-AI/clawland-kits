# DC Guardian — Bill of Materials

**Estimated total: $88.00 USD** (prices as of 2025, single-unit retail).

| # | Part | Spec | Qty | Unit | Supplier link | Notes |
|---|------|------|-----|------|---------------|-------|
| 1 | LicheeRV-Nano | RISC-V SBC, 40-pin header, Wi-Fi | 1 | $35.00 | [Sipeed](https://sipeed.com/) | Any LicheeRV-Nano revision with GPIO header |
| 2 | DHT22 / AM2302 | Digital temp + humidity, 3.3–5 V | 1 | $6.00 | [Adafruit #385](https://www.adafruit.com/product/385) | Prefer the bare sensor over the 3-pin module for accuracy |
| 3 | MQ-2 module | Smoke / LPG / methane, analog + digital out | 1 | $5.00 | [Generic](https://www.aliexpress.com/w/wholesale-mq-2-sensor.html) | Needs 5 V heater supply |
| 4 | Water leak probe | Resistive trace, 2-wire | 1 | $4.00 | [Generic](https://www.aliexpress.com/w/wholesale-water-leak-sensor.html) | Or DIY from perfboard + tinned traces |
| 5 | Power supply | 5 V / 2 A, barrel jack | 1 | $8.00 | [Generic](https://www.aliexpress.com/w/wholesale-5v-2a-power-supply.html) | Must be a real PSU, not a USB charger |
| 6 | microSD card | 32 GB, Class 10 | 1 | $7.00 | [Generic](https://www.aliexpress.com/w/wholesale-32gb-microsd.html) | PicoClaw image target |
| 7 | Enclosure | ABS, ≥ 100 × 68 × 50 mm, DIN or wall | 1 | $9.00 | [Generic](https://www.aliexpress.com/w/wholesale-abs-enclosure.html) | IP54 or better |
| 8 | Jumper wires + terminal blocks | 22 AWG, 2-pin screw terminals | 1 | $3.00 | [Generic](https://www.aliexpress.com/w/wholesale-22awg-jumper-wire.html) | |
| 9 | Perfboard + standoffs | 5 × 7 cm, M3 nylon | 1 | $4.00 | [Generic](https://www.aliexpress.com/w/wholesale-perfboard.html) | |
| 10 | Misc | Heat-shrink, 500 mA fuse, cable ties, cable gland | 1 | $7.00 | [Generic](https://www.aliexpress.com/w/wholesale-heat-shrink-tubing.html) | Fuse goes inline on the 5 V feed |
| | **Total** | | | **$88.00** | | |

## Substitutions

- **DHT22 → SHT31** (+$6): better accuracy and a true I²C interface. Update `skill.yaml` to the `sht31` driver.
- **MQ-2 → MQ-2 bare sensor**: cheaper, but you must build the load-resistor divider yourself.
- **Water leak probe → DS18B20 + probe**: only if you also want floor temperature; the leak function is lost.

## Not Included

- Network drop or Wi-Fi credentials
- SIM / SMS credits (only if you enable the SMS escalation step)
- Fire-rated cabling

## Sourcing Notes

All parts are commodity items. Buy two of each sensor — they are the failure points, and a spare costs less than a second shipping round.
