# DC Guardian — Data Center Night-Shift Monitoring Kit

> **$88 kit** replaces a **$48,000/year** data center night-shift operator.

Monitors temperature, humidity, smoke/gas, and water leaks across a small-to-medium data center floor. Sends real-time alerts via PicClaw when thresholds are breached.

---

## At a Glance

| | |
|-|-|
| **Board** | Sipeed LicheeRV-Nano (RISC-V, 512 MB DDR3) |
| **Sensors** | DHT22 (temp/humidity), MQ-2 (smoke/gas), Water leak × 2 |
| **Alert output** | Piezo buzzer (local) + PicClaw webhook (remote) |
| **Kit cost** | ~$88 USD |
| **Replaces** | $48,000/yr data center night-shift operator |
| **ROI break-even** | < 1 day |
| **Coverage area** | 1–4 rack rows (expand with additional sensor nodes) |

---

## What It Monitors

| Condition | Sensor | Default Threshold | Action |
|-----------|--------|:-----------------:|--------|
| High temperature | DHT22 | > 27 °C (80.6 °F) | Warn |
| Critical temperature | DHT22 | > 32 °C (89.6 °F) | Alert + buzzer |
| High humidity | DHT22 | > 60% RH | Warn |
| Low humidity | DHT22 | < 20% RH | Warn (static risk) |
| Smoke / gas detected | MQ-2 | DO pin LOW | Alert + buzzer |
| Water leak (zone 1) | Water sensor 1 | signal HIGH | Alert + buzzer |
| Water leak (zone 2) | Water sensor 2 | signal HIGH | Alert + buzzer |

All thresholds are configurable in `alerts.yaml`.

---

## Files in This Kit

```
kits/dc-guardian/
├── README.md          ← You are here
├── BOM.md             ← Full parts list with purchase links
├── WIRING.md          ← Connection diagram (ASCII + pin table)
├── skill.yaml         ← PicClaw skill configuration
├── alerts.yaml        ← Alert thresholds and escalation rules
└── drivers/
    ├── dht22.py       ← DHT22 driver (single-wire)
    ├── mq2_smoke.py   ← MQ-2 digital-out smoke detector
    └── water_leak.py  ← Resistive water sensor reader
```

---

## Prerequisites

- Soldering iron (optional — breadboard build requires none)
- MicroSD card reader (to flash PicClaw image)
- USB-C power adapter (5 V / 3 A minimum)
- WiFi network credentials for the data center (or Ethernet via USB adapter)

---

## Assembly Instructions

### Step 1 — Flash PicClaw to the MicroSD Card

**Time: ~10 minutes**

1. Download the LicheeRV-Nano PicClaw image:
   ```
   picclaw image download licheerv-nano --kit dc-guardian
   ```
   Or download manually from the [PicClaw releases page](https://github.com/Clawland-AI/picclaw/releases).

2. Insert the MicroSD card into your card reader.

3. Flash the image using Balena Etcher (GUI) or `dd` (CLI):
   ```bash
   # macOS / Linux
   sudo dd if=picclaw-licheerv-nano.img of=/dev/sdX bs=4M status=progress
   ```
   > Replace `/dev/sdX` with your card device. Use `lsblk` or Disk Utility to confirm.

4. After flashing, mount the `BOOT` partition and edit `picclaw.conf`:
   ```ini
   [wifi]
   ssid = YOUR_DATACENTER_SSID
   password = YOUR_PASSWORD

   [skill]
   name = dc-guardian
   ```

5. Eject the card safely.

---

### Step 2 — Wire the Sensors on the Breadboard

**Time: ~20 minutes**

See [WIRING.md](WIRING.md) for the full diagram. Summary:

```
Component       Board Pin    Notes
──────────────────────────────────────────────────────
DHT22 VCC    →  Pin 1 (3.3V)
DHT22 GND    →  Pin 6 (GND)
DHT22 DATA   →  Pin 11 (GPIO_A28)   + 4.7 kΩ pull-up to 3.3V
──────────────────────────────────────────────────────
MQ-2 VCC     →  Pin 2 (5V)          Heater needs 5V
MQ-2 GND     →  Pin 6 (GND)
MQ-2 DO      →  Pin 13 (GPIO_A29)   Digital threshold output
──────────────────────────────────────────────────────
Water S1 VCC →  Pin 17 (3.3V)
Water S1 GND →  Pin 9 (GND)
Water S1 SIG →  Pin 15 (GPIO_A30)
──────────────────────────────────────────────────────
Water S2 VCC →  Pin 17 (3.3V)
Water S2 GND →  Pin 9 (GND)
Water S2 SIG →  Pin 16 (GPIO_A31)
──────────────────────────────────────────────────────
Buzzer (+)   →  Pin 18 (GPIO_B0)
Buzzer (-)   →  Pin 9 (GND)
```

**Pull-up resistor:**
On the breadboard, connect a 4.7 kΩ resistor between the DHT22 DATA row and the 3.3V rail. This is required — the DHT22 will not communicate without it.

**Breadboard layout tips:**
- Use the left power rail for 3.3V (red wire from pin 1 and pin 17).
- Use the right power rail for 5V (orange wire from pin 2) — keep this separate to avoid accidentally powering 3.3V-only components from 5V.
- Group each sensor in its own 5-row section of the breadboard.

> **Photo checkpoint:** Before powering on, visually trace each wire from the LicheeRV-Nano header to the sensor. Confirm no bare wire ends are touching adjacent pins.

---

### Step 3 — Insert MicroSD and First Boot

**Time: ~5 minutes**

1. Insert the flashed MicroSD card into the LicheeRV-Nano's card slot (underside of the board).
2. Connect the USB-C power cable from the PSU to the board.
3. The board will boot. The green LED will blink, then hold solid when PicClaw is running (~30 seconds).
4. Wait an additional 60 seconds for the MQ-2 heater to warm up. During this window, smoke alerts are suppressed automatically.

---

### Step 4 — Verify Sensor Readings

**Time: ~5 minutes**

SSH into the board or use the PicClaw CLI on the same network:

```bash
picclaw status --kit dc-guardian
```

Expected output:
```
DC Guardian v1.0.0
  temperature:  22.4 °C  ✓
  humidity:     41.2 %RH ✓
  smoke (MQ-2): CLEAR     ✓
  water zone 1: DRY       ✓
  water zone 2: DRY       ✓
  buzzer:       STANDBY   ✓
  uptime:       00:01:24
```

If a sensor shows `ERR`:
- **DHT22 ERR** → Check pull-up resistor and DATA wire (pin 11)
- **MQ-2 ERR** → Verify 5V on MQ-2 VCC; allow 60 s warm-up
- **WATER ERR** → Check VCC/GND polarity on sensor module

---

### Step 5 — Mount in Enclosure

**Time: ~15 minutes**

1. Drill two 12 mm holes in the enclosure lid for cable glands (one per sensor run).
2. Thread the water sensor cables through the glands before tightening them down.
3. Secure the LicheeRV-Nano and breadboard inside the enclosure using M2.5 standoffs or double-sided foam tape.
4. Mount the buzzer through a small hole in the enclosure side (or leave internal — it's loud enough).
5. Route the USB-C power cable through a third cable gland or a notch in the enclosure base.
6. Close the lid and fasten the screws.

---

### Step 6 — Deploy in the Data Center

1. Mount the enclosure on a rack post or wall near the center of the monitored zone — typically at mid-rack height.
2. Route water sensor cables to:
   - **Zone 1:** Under the CRAC/CRAH unit drain pan
   - **Zone 2:** Under the UPS battery bank or near any condensate drain
3. Position the DHT22 away from direct airflow (it measures ambient, not supply air).
4. The MQ-2 should face upward — smoke rises.
5. Confirm the board has WiFi signal at the install location:
   ```bash
   picclaw ping --kit dc-guardian
   ```

---

### Step 7 — Configure Alerts

Edit `alerts.yaml` and push to the board:

```bash
picclaw config push alerts.yaml --kit dc-guardian
```

Restart the skill to apply:

```bash
picclaw skill restart dc-guardian
```

---

## Maintenance

| Task | Frequency | Notes |
|------|-----------|-------|
| Verify readings via `picclaw status` | Weekly | Should take < 1 min |
| MQ-2 recalibration | Every 6 months | Run in clean air for 24 h, note baseline |
| Water sensor cleaning | Every 3 months | Wipe contacts with isopropyl alcohol |
| DHT22 accuracy check | Annually | Compare against reference thermometer |
| MicroSD card replacement | Every 2–3 years | Write endurance limit |

---

## ROI Calculation

| | Annual Cost |
|-|------------:|
| Data center night-shift operator (US avg) | $48,000 |
| DC Guardian kit (one-time) | $88 |
| **Year 1 savings** | **$47,912** |
| **3-year savings** | **$143,736** |

> The kit pays for itself in under 40 minutes of the first shift it replaces.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No boot (no LED) | Bad MicroSD flash or no power | Reflash card; check PSU |
| DHT22 reads −40 °C | Missing pull-up resistor | Add 4.7 kΩ between DATA and 3.3V |
| MQ-2 always triggering | Sensitivity too high or still warming | Turn pot CW; wait 2 min |
| MQ-2 never triggers (smoke test) | Sensitivity too low | Turn pot CCW |
| Water sensor always wet | Sensor contacts corroded | Clean with IPA; replace if needed |
| WiFi not connecting | Wrong credentials | Re-edit picclaw.conf and reflash |
| Buzzer not sounding | GPIO polarity | Check buzzer is *active* type (not passive) |
