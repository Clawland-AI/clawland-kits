# Greenhouse Pro Bill Of Materials

Prices are typical US online retail prices as of May 2026. Use equivalent modules when pinout, voltage, and interface are compatible.

| Item | Qty | Unit | Est. total | Purpose | Example source |
| --- | ---: | ---: | ---: | --- | --- |
| LicheeRV-Nano or PicClaw-compatible edge board | 1 | USD 29.00 | USD 29.00 | Main controller | https://wiki.sipeed.com/hardware/en/lichee/RV_Nano/ |
| BME280 I2C module | 1 | USD 6.50 | USD 6.50 | Air temperature, humidity, pressure | https://www.adafruit.com/product/2652 |
| Capacitive soil moisture sensor v2 | 2 | USD 4.50 | USD 9.00 | Bed moisture monitoring | https://www.dfrobot.com/product-1385.html |
| BH1750 I2C light sensor | 1 | USD 3.50 | USD 3.50 | Lux and light exposure | https://www.sparkfun.com/products/13688 |
| SCD41 CO2 sensor module | 1 | USD 29.95 | USD 29.95 | CO2 and ventilation signal | https://www.adafruit.com/product/5190 |
| DS18B20 waterproof temperature probe | 1 | USD 6.95 | USD 6.95 | Leaf or reservoir temperature | https://www.adafruit.com/product/381 |
| 2-channel opto-isolated relay module | 1 | USD 6.00 | USD 6.00 | Fan and pump switching | https://www.amazon.com/s?k=2+channel+opto+isolated+relay+module |
| 5 V 2 A power supply | 1 | USD 8.00 | USD 8.00 | Controller and relay power | https://www.adafruit.com/product/276 |
| JST or screw terminal breakout kit | 1 | USD 5.00 | USD 5.00 | Field wiring | https://www.adafruit.com/product/2138 |
| 4.7 kOhm resistor pack | 1 | USD 1.50 | USD 1.50 | DS18B20 pull-up | https://www.adafruit.com/product/2783 |
| Waterproof cable glands | 4 | USD 1.25 | USD 5.00 | Enclosure strain relief | https://www.digikey.com/en/products/filter/cable-and-cord-grips/492 |
| IP65 plastic enclosure, about 120 x 80 x 50 mm | 1 | USD 12.00 | USD 12.00 | Electronics housing | https://www.polycase.com/waterproof-enclosures |

## Cost Summary

| Category | Cost |
| --- | ---: |
| Controller | USD 29.00 |
| Sensors | USD 55.90 |
| Actuation | USD 6.00 |
| Power and wiring | USD 19.50 |
| Enclosure | USD 12.00 |
| Estimated kit total | USD 122.40 |

The bounty board target calls for a complete hardware design rather than a strict cost ceiling. The design can be reduced to about USD 93 by replacing the SCD41 with an optional MQ-135-style qualitative air sensor, but the SCD41 is recommended for repeatable greenhouse CO2 readings.

## Substitutions

- Controller: ESP32-S3 can replace LicheeRV-Nano when PicClaw ESP32 firmware is used.
- CO2: Senseair S8 can replace SCD41 over UART if higher accuracy is required.
- Soil probes: use capacitive probes only; resistive probes corrode quickly in greenhouse beds.
- Relay: replace with a MOSFET board for DC pumps below the board's current rating.

