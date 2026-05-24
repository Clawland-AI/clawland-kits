# DC Guardian — Wiring Guide

> **Data Center Night Shift Monitoring Kit — Complete Wiring Diagram**
> LicheeRV-Nano + DHT22 ×2 + MQ-2 Smoke + Water Leak Sensors + Buzzer + LEDs

---

## Overview

The DC Guardian uses the LicheeRV-Nano's GPIO pins to interface with:
- **2× DHT22** sensors (temperature + humidity at rack inlet and exhaust)
- **1× MQ-2** smoke/gas sensor (fire detection)
- **2× Water leak** sensors (flooding detection near cooling units)
- **1× Piezo buzzer** (local alarm)
- **2× LEDs** (status indicators)

---

## LicheeRV-Nano Pin Reference

The LicheeRV-Nano (Allwinner R528) exposes GPIO via a 40-pin header:

```
        ┌─────────────────────────────┐
        │      LicheeRV-Nano          │
        │      (Top View)             │
        │                             │
        │  ┌─Pin 1              Pin 40─┐
        │  │ ● 3.3V            5V ● │
        │  │ ● GPIO_PD18    5V  ● │
        │  │ ● GPIO_PD16    GND ● │
        │  │ ● GPIO_PD14   GPIO_PB3 ● │
        │  │ ● GPIO_PD12   GND ● │
        │  │ ● GPIO_PD10  GPIO_PB1 ● │
        │  │ ● 3.3V       GPIO_PB0 ● │
        │  │ ● GPIO_PD8   GPIO_PB2 ● │
        │  │ ● GND        GPIO_PB4 ● │
        │  │ ● GPIO_PD6   GND ● │
        │  │ ● GPIO_PD4  GPIO_PB5 ● │
        │  │ ● GPIO_PD2  GPIO_PB6 ● │
        │  │ ● GND       GPIO_PB7 ● │
        │  │ ● GPIO_PD0    GND ● │
        │  │ ● GPIO_PC7  GPIO_PC8 ● │
        │  │ ● GPIO_PC5  GPIO_PC9 ● │
        │  │ ● 3.3V      GPIO_PC10 ● │
        │  │ ● GPIO_PC3  GPIO_PC11 ● │
        │  │ ● GPIO_PC1     GND ● │
        │  │ ● GND       GPIO_PC13 ● │
        │  └─Pin 2              Pin 39─┘
        │                             │
        └─────────────────────────────┘
```

---

## Pin Assignment Table

| GPIO Pin | Function | Connected To | Direction | Notes |
|----------|----------|-------------|-----------|-------|
| **PD18** | I2C_SDA / GPIO | DHT22 #1 (Inlet) Data | Input | 4.7kΩ pull-up to 3.3V |
| **PD16** | I2C_SCL / GPIO | DHT22 #2 (Exhaust) Data | Input | 4.7kΩ pull-up to 3.3V |
| **PD14** | SPI_MOSI / GPIO | MQ-2 Smoke Analog (via ADC) | Input | Direct connection if ADC available |
| **PD12** | SPI_MISO / GPIO | MQ-2 Smoke Digital | Input | Threshold-based detection |
| **PD10** | SPI_CLK / GPIO | Water Leak #1 (Floor) | Input | 10kΩ pull-down to GND |
| **PD8** | SPI_CS / GPIO | Water Leak #2 (Cooling Unit) | Input | 10kΩ pull-down to GND |
| **PD6** | UART_TX / GPIO | Buzzer Control | Output | Via 2N2222 NPN transistor |
| **PD4** | UART_RX / GPIO | Red LED (Alarm) | Output | 220Ω current limiter |
| **PD2** | GPIO | Green LED (System OK) | Output | 220Ω current limiter |
| **PD0** | GPIO | Reserved (OLED SDA) | — | For optional display |
| **PC7** | GPIO | Reserved (OLED SCL) | — | For optional display |

---

## Wiring Diagram (ASCII)

```
                    LicheeRV-Nano Board
                    ┌──────────────────┐
                    │                  │
    5V ──────────── │ 5V           GND │ ───────────── GND Bus
                    │                  │
    DHT22 #1 ───── │ PD18         3V3 │ ───┬──────── 3.3V Bus
    (Inlet)         │                  │    │
    DHT22 #2 ───── │ PD16          PB3 │    │
    (Exhaust)       │                  │    │
    MQ-2 DOUT ──── │ PD12          GND │    │
                    │                  │    │
    Water #1 ───── │ PD10         PB1 │    │
    (Floor)         │                  │    │
    Water #2 ───── │ PD8          PB0 │    │
    (Cooling)       │                  │    │
                    │ PD6 ──────┐      │    │  (Buzzer via transistor)
                    │           │      │    │
    Red LED ─────── │ PD4       │      │    │
    Green LED ───── │ PD2       │      │    │
                    │           │      │    │
                    └───────────┼──────┘    │
                                │           │
                                ▼           │
                        ┌──────────┐        │
                        │ 2N2222   │        │
                        │ NPN      │        │
                        │          │        │
                        │ B ───┤   │        │
                        │ E ───┤───┼────────┘
                        │ C ───┤   │
                        │      │   │
                        └──┬───┘   │
                           │       │
                           ▼       │
                        [BUZZER]   │
                           │       │
                          GND      │
                                   │
    ┌──────────────────────────────┘
    │
    ▼
    GND Bus (common ground for all sensors)
```

---

## Detailed Connection Guide

### 1. DHT22 #1 — Rack Inlet Temperature/Humidity

```
DHT22 Pin 1 (VCC)  ──→  3.3V Bus
DHT22 Pin 2 (DATA) ──→  PD18 ──→ 4.7kΩ ──→ 3.3V (pull-up)
DHT22 Pin 3 (NC)   ──→  Not Connected
DHT22 Pin 4 (GND)  ──→  GND Bus

Wire Color Convention:
  Red   = VCC (3.3V)
  White = DATA
  Black = GND
```

**Placement:** Mount at the **cold air intake** of the rack, 10–15cm above floor level. Avoid direct airflow from fans.

### 2. DHT22 #2 — Rack Exhaust Temperature/Humidity

```
DHT22 Pin 1 (VCC)  ──→  3.3V Bus
DHT22 Pin 2 (DATA) ──→  PD16 ──→ 4.7kΩ ──→ 3.3V (pull-up)
DHT22 Pin 3 (NC)   ──→  Not Connected
DHT22 Pin 4 (GND)  ──→  GND Bus
```

**Placement:** Mount at the **hot air exhaust** of the rack, near the top. The temperature differential (ΔT) between inlet and exhaust indicates cooling efficiency.

### 3. MQ-2 Smoke/Gas Sensor

```
MQ-2 VCC      ──→  5V Bus (requires 5V for heater)
MQ-2 GND      ──→  GND Bus
MQ-2 DOUT     ──→  PD12 (digital threshold output)
MQ-2 AOUT     ──→  PD14 (analog output, if ADC available)

Note: MQ-2 heater draws ~150mA. Ensure 5V supply has adequate current.
```

**Placement:** Mount at **ceiling level** (smoke rises) or near the top of the rack. Keep away from direct airflow from fans to prevent false readings. Allow 48-hour burn-in before relying on readings.

### 4. Water Leak Sensor #1 — Floor

```
Water Sensor Probe Wire 1 ──→  PD10
Water Sensor Probe Wire 2 ──→  GND Bus

PD10 ──→ 10kΩ ──→ GND (pull-down, ensures LOW when no water)

Logic:
  No water  → PD10 reads LOW (pulled down)
  Water detected → PD10 reads HIGH (water conducts between probes)
```

**Placement:** Place flat on the **floor** beneath the rack, near pipe joints and cooling unit drip trays.

### 5. Water Leak Sensor #2 — Cooling Unit

```
Water Sensor Probe Wire 1 ──→  PD8
Water Sensor Probe Wire 2 ──→  GND Bus

PD8 ──→ 10kΩ ──→ GND (pull-down)
```

**Placement:** Place directly under the **CRAC/CRAH unit** or any cooling infrastructure with water lines.

### 6. Buzzer (via NPN Transistor)

```
         PD6 (GPIO Output)
          │
          ▼
    ┌─── 1kΩ ───┐
    │            │
    │     ┌──────┤ Base
    │     │      │
    │     │   2N2222 NPN
    │     │      │
    │     │   Collector
    │     │      │
    │     │      ├──→ Buzzer (+)
    │     │      │         │
    │     │      │    Buzzer (-)
    │     │      │         │
    │     │      │        GND
    │     │      │
    │     └──────┤ Emitter
    │            │
    │           GND
    │
    5V Bus ──→ Buzzer VCC (+)
```

**Purpose:** Provides audible alarm when smoke or water is detected, even if the network is down.

### 7. Status LEDs

```
PD4 ──→ 220Ω ──→ Red LED (Anode) ──→ GND (Cathode)
        Alarm indicator: ON when alert condition detected

PD2 ──→ 220Ω ──→ Green LED (Anode) ──→ GND (Cathode)
        Status indicator: ON when system is healthy, BLINK when sampling
```

---

## Power Distribution

```
5V USB-C PSU
    │
    ├──→ LicheeRV-Nano (5V input)
    │
    ├──→ MQ-2 Sensor (5V, ~150mA heater)
    │
    └──→ 5V Bus (breadboard power rail)
              │
              ├──→ Buzzer (5V)
              │
              └──→ 3.3V Regulator (on LicheeRV-Nano)
                        │
                        ├──→ DHT22 #1 (3.3V, ~1.5mA)
                        ├──→ DHT22 #2 (3.3V, ~1.5mA)
                        ├──→ Water Sensors (3.3V logic)
                        └──→ LEDs (via 3.3V GPIO)
```

**Total current draw:** ~200mA typical, ~350mA peak (MQ-2 heater active). Use a 5V/3A PSU for headroom.

---

## Breadboard Layout (Top View)

```
    + ──────────────────────────────────────────── +
    │  5V Rail                                     │
    │                                              │
a   │  [MQ-2 VCC]  [Buzzer VCC]                   │
b   │                                              │
c   │                                              │
d   │                                              │
e   │                                              │
    │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
    │                                              │
f   │  [DHT22#1 VCC] [DHT22#2 VCC] [3.3V]        │
g   │                                              │
h   │  [DHT22#1 DAT] [DHT22#2 DAT]               │
i   │   ↕4.7kΩ→3.3V  ↕4.7kΩ→3.3V                │
j   │                                              │
    │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
    │                                              │
k   │  [Water#1]    [Water#2]    [Red LED] [Green] │
l   │   ↕10kΩ→GND   ↕10kΩ→GND   ↕220Ω    ↕220Ω  │
m   │                                              │
n   │  [MQ-2 DOUT]  [2N2222]                      │
o   │                 ↕1kΩ→PD6                     │
    │                                              │
    │  GND Rail                                    │
    - ──────────────────────────────────────────── -
```

---

## Wiring Checklist

- [ ] All GND connections share a common ground bus
- [ ] 3.3V and 5V rails are NOT connected to each other
- [ ] DHT22 pull-up resistors (4.7kΩ) are in place
- [ ] Water sensor pull-down resistors (10kΩ) are in place
- [ ] LED current-limiting resistors (220Ω) are in place
- [ ] Buzzer transistor base resistor (1kΩ) is in place
- [ ] MQ-2 sensor is on the 5V rail (not 3.3V)
- [ ] No loose wires or short circuits on breadboard
- [ ] All Dupont connectors are fully seated
- [ ] Cable ties used to secure wires to rack

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| DHT22 reads NaN | Missing pull-up resistor | Add 4.7kΩ between DATA and 3.3V |
| DHT22 reads -40°C | Sensor too close to heat source | Relocate away from exhaust |
| MQ-2 false alarms | Insufficient burn-in | Wait 48 hours, recalibrate |
| Water sensor always HIGH | Probe corroded or bridged | Clean probes, check for mineral buildup |
| Buzzer doesn't sound | Transistor wired incorrectly | Check BCE pinout of 2N2222 |
| LEDs dim | Resistor too high | Use 150Ω instead of 220Ω |
| Board won't boot | Insufficient power | Use 5V/3A PSU, not 5V/1A |
| Intermittent readings | Loose breadboard connections | Re-seat all jumper wires |

---

## Safety Notes

⚠️ **This kit is NOT a replacement for certified fire suppression systems.**
⚠️ **The MQ-2 sensor detects combustible gases, not all fire types.**
⚠️ **Always maintain existing safety infrastructure.**
⚠️ **Test the system monthly with simulated conditions.**

---

## Next Steps

1. Wire everything according to this guide
2. Flash the LicheeRV-Nano with PicClaw firmware
3. Install the DC Guardian skill: `picclaw skill install dc-guardian`
4. Configure alert thresholds in `alerts.yaml`
5. Run the self-test: `picclaw test dc-guardian --self-test`
6. Deploy to your data center

---

*Part of the [Clawland Kits](https://github.com/Clawland-AI/clawland-kits) project — Open hardware sensor kits for edge AI monitoring.*
*Licensed under [CERN-OHL-S-2.0](https://ohwr.org/cernohl).*
