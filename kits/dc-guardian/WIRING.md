# DC Guardian — Wiring Guide

Complete connection diagram for the data center monitoring kit.

---

## Pin Reference — LicheeRV-Nano

| Function | GPIO Pin | Notes |
|----------|----------|-------|
| 3.3V Power Out | Pin 1 (3V3) | Powers sensors |
| 5V Power Out | Pin 2 (5V) | Powers MQ-2 heaters |
| Ground | Pin 6 (GND) | Common ground |
| I2C SDA | GPIO_12 | DHT22 #1 (data center hot aisle) |
| I2C SCL | GPIO_13 | DHT22 #2 (data center cold aisle) |
| Analog In 0 | GPIO_14 (A0) | MQ-2 #1 (smoke detector 1) |
| Analog In 1 | GPIO_15 (A1) | MQ-2 #2 (smoke detector 2) |
| Digital In 0 | GPIO_16 | Water sensor #1 (under raised floor) |
| Digital In 1 | GPIO_17 | Water sensor #2 (near cooling pipes) |

---

## Wiring Diagram (ASCII)

```
┌──────────────────────────────────────────────────────────────────────┐
│                    DC GUARDIAN — WIRING DIAGRAM                      │
│                                                                      │
│   ┌─────────────────────┐                                            │
│   │   LICHEERV-NANO     │                                            │
│   │                     │                                            │
│   │  3V3 (Pin1) ────────┼─────────┬────────────┬──────────┐         │
│   │                     │         │            │          │         │
│   │  5V  (Pin2) ────────┼─────┬───┘            │          │         │
│   │                     │     │                │          │         │
│   │  GND (Pin6) ────────┼─┬───┼────────────────┼──────────┼────┐    │
│   │                     │ │   │                │          │    │    │
│   │  GPIO_12 ───────────┼─┼───┼────────────────┼──────────┤    │    │
│   │  GPIO_13 ───────────┼─┼───┼────────────────┼──────────┤    │    │
│   │  GPIO_14 (A0) ──────┼─┼───┼────┐           │          │    │    │
│   │  GPIO_15 (A1) ──────┼─┼───┼────┼───┐       │          │    │    │
│   │  GPIO_16 ───────────┼─┼───┼────┼───┼───┐   │          │    │    │
│   │  GPIO_17 ───────────┼─┼───┼────┼───┼───┼───┐│          │    │    │
│   └─────────────────────┘ │   │    │   │   │   ││          │    │    │
│                           │   │    │   │   │   ││          │    │    │
│    ┌──────┐    ┌──────┐   │   │    │   │   │   ││          │    │    │
│    │DHT22 │    │DHT22 │   │   │    │   │   │   ││          │    │    │
│    │  #1  │    │  #2  │   │   │    │   │   │   ││          │    │    │
│    │HOT   │    │COLD  │   │   │    │   │   │   ││          │    │    │
│    │AISLE │    │AISLE │   │   │    │   │   │   ││          │    │    │
│    └──┬───┘    └──┬───┘   │   │    │   │   │   ││          │    │    │
│       │ VCC      │ VCC ───┘   │    │   │   │   ││          │    │    │
│       │ DATA     │ DATA ──────┘    │   │   │   ││          │    │    │
│       │ GND      │ GND ───────────┼───┼───┼───┼┤          │    │    │
│       └──┘       └──┘              │   │   │   ││          │    │    │
│                                     │   │   │   ││          │    │    │
│    ┌──────┐    ┌──────┐            │   │   │   ││          │    │    │
│    │ MQ-2 │    │ MQ-2 │            │   │   │   ││          │    │    │
│    │  #1  │    │  #2  │            │   │   │   ││          │    │    │
│    │NEAR  │    │CABLE │            │   │   │   ││          │    │    │
│    │CRAC  │    │TRAY  │            │   │   │   ││          │    │    │
│    └──┬───┘    └──┬───┘            │   │   │   ││          │    │    │
│       │ VCC      │ VCC ────────────┘   │   │   ││          │    │    │
│       │ A0       │ A1 ─────────────────┘   │   ││          │    │    │
│       │ GND      │ GND ────────────────────────┤          │    │    │
│       └──┘       └──┘                         │          │    │    │
│                                                 │          │    │    │
│    ┌──────┐    ┌──────┐                         │          │    │    │
│    │WATER │    │WATER │                         │          │    │    │
│    │  #1  │    │  #2  │                         │          │    │    │
│    │RAISED │    │COOLNG│                         │          │    │    │
│    │FLOOR │    │PIPES │                         │          │    │    │
│    └──┬───┘    └──┬───┘                         │          │    │    │
│       │ VCC      │ VCC ─────────────────────────┘          │    │    │
│       │ DO       │ DO ─────────────────────────────────────┘    │    │
│       │ GND      │ GND ──────────────────────────────────────────┘    │
│       └──┘       └──┘                                                   │
│                                                                         │
│   ⚡ POWER: USB-C 5V/3A ──────────────────────────────────────────────│
│   🌐 NETWORK: Ethernet (Cat6) or WiFi                                  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Connection Details

### DHT22 Temperature/Humidity Sensors

**Sensor #1 (Hot Aisle):**
| Sensor Pin | Wire Color | Connect To |
|-----------|-----------|------------|
| VCC (+) | Red | LicheeRV Pin 1 (3.3V) |
| DATA OUT | Yellow | LicheeRV GPIO_12 + 10kΩ pull-up to 3.3V |
| GND (-) | Black | LicheeRV Pin 6 (GND) |

**Sensor #2 (Cold Aisle):**
| Sensor Pin | Wire Color | Connect To |
|-----------|-----------|------------|
| VCC (+) | Red | LicheeRV Pin 1 (3.3V) |
| DATA OUT | Yellow | LicheeRV GPIO_13 + 10kΩ pull-up to 3.3V |
| GND (-) | Black | LicheeRV Pin 6 (GND) |

> ⚠️ **Important:** Each DHT22 data line needs a **10kΩ pull-up resistor** between DATA and VCC.

### MQ-2 Smoke/Gas Sensors

**Sensor #1 (Near CRAC unit):**
| Module Pin | Connect To |
|-----------|------------|
| VCC | LicheeRV 5V (Pin 2) |
| GND | LicheeRV GND (Pin 6) |
| A0 (Analog Out) | LicheeRV GPIO_14 (A0) |
| D0 (Digital Out) | Not connected (use analog for precision) |

**Sensor #2 (Cable trays):**
| Module Pin | Connect To |
|-----------|------------|
| VCC | LicheeRV 5V (Pin 2) |
| GND | LicheeRV GND (Pin 6) |
| A0 (Analog Out) | LicheeRV GPIO_15 (A1) |
| D0 (Digital Out) | Not connected |

> ⚠️ **Warm-up:** MQ-2 sensors require **20 minutes** to stabilize after power-on. During warm-up, readings may be inaccurate.

### Water Leak Sensors

**Sensor #1 (Under raised floor):**
| Module Pin | Connect To |
|-----------|------------|
| VCC | LicheeRV 3.3V (Pin 1) |
| GND | LicheeRV GND (Pin 6) |
| DO (Digital Out) | LicheeRV GPIO_16 |

**Sensor #2 (Near cooling pipes):**
| Module Pin | Connect To |
|-----------|------------|
| VCC | LicheeRV 3.3V (Pin 1) |
| GND | LicheeRV GND (Pin 6) |
| DO (Digital Out) | LicheeRV GPIO_17 |

---

## Assembly Instructions

### Step 1: Prepare the Enclosure
1. Drill or cut **4 cable glands** in the enclosure sides for sensor cables
2. Cut **1 opening** for the USB-C power cable
3. Cut **1 opening** for the Ethernet cable
4. Mount the LicheeRV-Nano inside using standoffs or double-sided tape

### Step 2: Breadboard Setup
1. Place the LicheeRV-Nano at one end of the breadboard
2. Create **power rails**: connect 3.3V and 5V to breadboard power buses
3. Connect **ground bus**: wire all GND pins together

### Step 3: Connect DHT22 Sensors
1. Insert each DHT22 into the breadboard
2. Wire VCC to 3.3V bus
3. Wire GND to ground bus
4. Connect DATA pin to respective GPIO with **10kΩ pull-up resistor**
5. Use long jumper wires (30cm+) to position sensors remotely

### Step 4: Connect MQ-2 Sensors
1. Wire each MQ-2 module: VCC → 5V bus, GND → ground bus
2. Connect A0 output to respective GPIO analog input
3. Position sensor modules in included plastic cases (they run warm)

### Step 5: Connect Water Sensors
1. Wire each water sensor: VCC → 3.3V, GND → ground, DO → GPIO
2. Route sensor probes through cable glands to monitoring positions

### Step 6: Power & Network
1. Connect USB-C power supply to LicheeRV-Nano
2. Connect Ethernet cable (or configure WiFi in `skill.yaml`)
3. Close the enclosure and verify all cable glands are sealed

### Step 7: Software Setup
1. Flash PicClaw onto the MicroSD card
2. Insert MicroSD into LicheeRV-Nano
3. Boot and verify network connectivity
4. Install the DC Guardian skill: `picclaw skill install dc-guardian`
5. Edit `alerts.yaml` with your notification endpoints (Slack webhook, SMS API, etc.)

---

## Physical Placement Guide

```
                    DATA CENTER LAYOUT (Top View)
   ┌─────────────────────────────────────────────────────┐
   │                                                       │
   │   ┌──────┐    HOT AISLE    ┌──────┐                  │
   │   │ RACK │  ┌──────────┐  │ RACK │                  │
   │   │  A   │  │ 🔴DHT22  │  │  B   │                  │
   │   │      │  │  #1      │  │      │                  │
   │   └──────┘  └──────────┘  └──────┘                  │
   │                                                       │
   │   ┌──────┐   COLD AISLE   ┌──────┐                  │
   │   │ RACK │  ┌──────────┐  │ RACK │    ┌───────────┐ │
   │   │  C   │  │ 🔵DHT22  │  │  D   │    │ 🟢LICHEE  │ │
   │   │      │  │  #2      │  │      │    │  RV-NANO  │ │
   │   └──────┘  └──────────┘  └──────┘    │  + ENCLOSR │ │
   │                                         └───────────┘ │
   │   ┌──────────┐ ┌──────────┐                           │
   │   │🟡MQ-2 #1 │ │🟡MQ-2 #2 │   ⚡ USB-C Power         │
   │   │ near CRAC│ │ cable try│   🌐 Ethernet to switch   │
   │   └──────────┘ └──────────┘                           │
   │                                                       │
   │   ┌──────────┐ ┌──────────┐                           │
   │   │💧WATER #1│ │💧WATER #2│                           │
   │   │under flr │ │cool pipes│                           │
   │   └──────────┘ └──────────┘                           │
   │                                                       │
   └─────────────────────────────────────────────────────┘
```

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| DHT22 reads NaN | Bad pull-up resistor | Check 10kΩ resistor between DATA and VCC |
| DHT22 reads -999°C | Sensor not responding | Check wiring, try a different GPIO |
| MQ-2 always reads high | Sensor not warmed up | Wait 20 minutes after power-on |
| MQ-2 reads zero | Module powered from 3.3V | MQ-2 needs **5V** for heater |
| Water sensor always triggers | Probe touching metal | Ensure probe is on dry, non-conductive surface |
| LicheeRV not booting | Bad SD card | Re-flash PicClaw image, verify SD integrity |
| No network | WiFi not configured | Check `skill.yaml` or use Ethernet |

---

## Safety Notes

- ⚡ **Do not exceed 5V** on LicheeRV-Nano GPIO pins (3.3V logic level)
- 🔥 **MQ-2 sensors run hot** (~40°C surface) — keep away from flammable materials
- 💧 **Keep LicheeRV-Nano dry** — mount in waterproof enclosure
- 🔌 **Use a UL-listed power supply** — data centers require certified equipment
- 📏 **Minimum sensor spacing**: 30cm between MQ-2 modules to avoid cross-talk
