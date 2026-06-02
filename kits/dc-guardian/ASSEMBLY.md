# 🔧 Assembly Instructions — DC Guardian

> **Estimated build time:** 45–75 minutes (bench) + 30 minutes (rack installation)
> **Skill level:** Intermediate — basic soldering, crimping, and multimeter use required
> **Wiring reference:** See [WIRING.md](WIRING.md) for diagrams and pin assignments before starting.

---

## 🧰 Tools Required

| Tool | Purpose |
|------|---------|
| Wire cutter/stripper (22–26 AWG) | Trimming and stripping sensor wires |
| Small flat‑head screwdriver (#00) | Terminal block screws |
| Digital multimeter | Continuity check, voltage verification, sensor test |
| Soldering iron (25W+) + solder | Resistor lead soldering, transistor wiring |
| Heat‑gun or lighter | Heat‑shrink tubing on soldered joints |
| Laptop with USB‑C | PicClaw flashing, serial console, SSH |

---

## Step 1 — Bench‑Check the Board

**Goal:** Verify the LicheeRV Nano boots and runs PicClaw.

1. **Flash PicClaw** (if not pre‑loaded):
   ```bash
   wget https://picclaw.io/releases/latest/picclaw-licheerv-nano.img.xz
   xzcat picclaw-licheerv-nano.img.xz | sudo dd of=/dev/sdX bs=4M status=progress
   sync
   ```
2. Insert microSD, connect USB‑C power, wait 30–60s for boot.
3. Verify:
   ```bash
   picclaw status
   # → agent=picclaw, version=X.Y.Z, uptime=N seconds
   ```

---

## Step 2 — Wire the Power Rails

1. Connect **3V3** (board pin 1) to breadboard **red (+)** rail.
2. Connect **GND** (board pin 39) to breadboard **blue (−)** rail.
3. Verify continuity: red rail to blue rail should read **open**.
4. Power on briefly and measure **3.25–3.35V** between rails.
5. **Power off** before connecting any sensors.

> ⚠️ Never connect or disconnect sensors while the board is powered.

---

## Step 3 — Wire I²C Bus (ADS1115)

1. Insert ADS1115 across breadboard center gap.
2. **VDD** → 3V3 rail · **GND** → GND rail · **SCL** → GPIO3 · **SDA** → GPIO2 · **ADDR** → GND (0x48).
3. Power on and scan:
   ```bash
   i2cdetect -y 0
   # → Should show device at 0x48
   ```

---

## Step 4 — Wire DHT22 Sensors (×2)

| Sensor | Pin | Connection |
|--------|-----|-----------|
| DHT22 #1 (room) | VCC → 3V3 · DATA → GPIO17 · GND → GND |
| DHT22 #2 (HVAC) | VCC → 3V3 · DATA → GPIO18 · GND → GND |

Add 10kΩ pull‑up from DATA to 3V3 if the module lacks one. Test:
```bash
python drivers/read_dht22.py --pin GPIO17 --name room
python drivers/read_dht22.py --pin GPIO18 --name hvac
```

---

## Step 5 — Wire DS18B20 Probe

- **Red** → 3V3 · **Yellow (DATA)** → GPIO19 · **Black** → GND
- **CRITICAL:** Solder a **4.7kΩ resistor** between GPIO19 and 3V3.
- Verify pull‑up: measure ~4.7kΩ between GPIO19 and 3V3.
- Test:
  ```bash
  python drivers/read_ds18b20.py --pin GPIO19
  # → {"ok": true, "temperature_c": 23.6}
  ```

---

## Step 6 — Wire Discrete Sensors

| Sensor | VCC | GND | DATA | GPIO |
|--------|-----|-----|------|------|
| MQ‑2 smoke/gas | 3V3 | GND | DO | GPIO21 |
| Water leak probe | 3V3 | GND | DO | GPIO20 |
| Reed switch #1 (rack door) | — | GND | one leg | GPIO22 |
| Reed switch #2 (room door) | — | GND | one leg | GPIO23 |

Enable internal pull‑UP on GPIO22/GPIO23 for reed switches. Test all:
```bash
python drivers/read_discrete.py --pin GPIO20 --name leak
python drivers/read_discrete.py --pin GPIO21 --name smoke
python drivers/read_discrete.py --pin GPIO22 --name door_rack
python drivers/read_discrete.py --pin GPIO23 --name door_room
```

---

## Step 7 — Wire Indicators

- **Buzzer:** GPIO24 → 1kΩ → Base(2N2222) · Emitter → GND · Collector → Buzzer(−) · Buzzer(+) → 3V3
- **Red LED:** GPIO25 → 330Ω → Anode · Cathode → GND
- **Green LED:** GPIO26 → 330Ω → Anode · Cathode → GND

Test:
```bash
picclaw gpio set GPIO24 high   # Buzzer ON
picclaw gpio set GPIO25 high   # Red ON
picclaw gpio set GPIO26 high   # Green ON
```

---

## Step 8 — Wire SCT‑013 Current Clamp

1. Plug SCT‑013 3.5mm jack: **tip (signal)** → ADS1115 A0 · **sleeve (GND)** → GND.
2. Do **not** add burden resistors (SCT‑013‑030 has internal burden).
3. Test:
   ```bash
   python drivers/read_sct013.py
   # → {"ok": true, "current_A": 0.0, "raw_adc": 16384}
   ```
4. Clamp around a powered device, re-run to see non‑zero current.

---

## Step 9 — Load the Scenario Config

```bash
picclaw skill install ./kits/dc-guardian
picclaw skill list
# → dc-guardian (version 1.0.0) should be listed
picclaw gateway
```

### Acceptance Tests

| Test | Method | Expected Result |
|------|--------|----------------|
| High temp | Warm DHT22 #1 with hand | Red LED ON, alert sent |
| Leak | Bridge leak probe with wet cloth | Red LED ON, buzzer sounds |
| Smoke | Press MQ‑2 test button (if available) | Red LED ON, buzzer sounds |
| Door open | Move magnet from reed switch | Alert after 60s |
| Current | Clamp around known load | Non‑zero current logged, Green LED ON |

---

## Step 10 — Install in the Rack Room

1. Power down and disconnect all USB cables.
2. Prepare the enclosure: drill holes for cable glands, mount board on standoffs.
3. Thread all sensor cables through glands with strain relief.
4. Place sensors per [placement rules](WIRING.md#-installation-placement-rules).
5. Secure cables with zip ties, label each cable, label the enclosure.
6. Restore power, verify boot, re‑run acceptance tests.

---

## ✅ Acceptance Checklist

```
☐ DHT22 #1 reports within ±0.5°C of reference
☐ DHT22 #2 reports within ±0.5°C of reference
☐ DS18B20 within ±0.5°C of DHT22 at same location
☐ Leak probe triggers alert when wet
☐ MQ‑2 smoke test triggers critical alert
☐ Reed switches register door state changes
☐ SCT‑013 current reading within ±5% of reference
☐ Buzzer sounds on critical alerts
☐ Red LED illuminates on warning/critical
☐ Green LED illuminates when all sensors normal
☐ Alerts reach Telegram/Discord within 10 seconds
☐ All cables labeled, enclosure closed and secured
```
