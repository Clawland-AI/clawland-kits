# DC Guardian — Wiring Guide

> **Power off before wiring.** Double-check polarity before applying 5 V.

## Pin Map (LicheeRV-Nano 40-pin header)

| Signal | Header pin | GPIO | Direction | Notes |
|--------|-----------|------|-----------|-------|
| 3.3 V | 1 | — | Power | DHT22 only |
| 5 V | 2 | — | Power | MQ-2 heater, via 500 mA fuse |
| GND | 6 | — | Ground | Common ground |
| DHT22 DATA | 7 | GPIO4 | Input | 10 kΩ pull-up to 3.3 V |
| MQ-2 DO | 11 | GPIO17 | Input | **Through 1 kΩ / 2 kΩ divider** |
| Leak probe A | 13 | GPIO27 | Input | Internal pull-up enabled |
| Leak probe B | 14 | — | Ground | |

## ASCII Diagram

```
                    +5V (pin 2) ---[500mA fuse]---+
                                                  |
                                            +-----+-----+
                                            |   MQ-2    |
                                            |  VCC  GND |
                                            +--+----+---+
                                               |    |
                    GND (pin 6) ---------------+    |
                                                    |
                              +---------------------+
                              |
                        +-----+-----+
                        | 1kΩ       |
                        | divider   |
                        +-----+-----+
                              |
                          GPIO17 (pin 11)
                              |
                        [2kΩ to GND]


   +3.3V (pin 1) ---+
                    |
                 [10kΩ]
                    |
   GPIO4 (pin 7) ---+---------- DATA  +-------------+
                    |                  |    DHT22    |
                    +------------------+  (front view)|
                                       +-------------+
   GND (pin 6) ------------------------ GND


   GPIO27 (pin 13) --------------------+~~~~~~~~~~~+
                                       | leak probe |
   GND (pin 14) -----------------------+~~~~~~~~~~~+
```

## MQ-2 Divider

The MQ-2 digital output swings to 5 V. The LicheeRV-Nano GPIO is 3.3 V only.

```
MQ-2 DO ---[1kΩ]---+--- GPIO17
                   |
                 [2kΩ]
                   |
                  GND
```

Output at GPIO17: 5 V × 2/(1+2) = **3.33 V**. Solder this inline and heat-shrink it — do not leave it on a breadboard inside the enclosure.

## DHT22 Pull-Up

Fit a 10 kΩ resistor between DATA and 3.3 V. Without it, reads fail intermittently at cable lengths over 30 cm.

## Leak Probe

Two tinned traces on perfboard, 2 mm apart, or a commercial probe. Dry = open, wet = ~10–100 kΩ. Enable the internal pull-up in `skill.yaml`; no external resistor needed.

## Cable Routing

- Sensor leads exit through the cable gland, never through the lid seam.
- Keep the DHT22 lead away from the 5 V feed — the heater current skews the reading.
- Maximum lead length: DHT22 1 m, MQ-2 1 m, leak probe 3 m.

## Continuity Check

Before power-on, with a multimeter:

1. 5 V (pin 2) to GND (pin 6): no short.
2. 3.3 V (pin 1) to GND (pin 6): no short.
3. GPIO17 to GND: reads ~2 kΩ (divider).
4. GPIO4 to 3.3 V: reads ~10 kΩ (pull-up).
