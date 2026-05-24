# DC Guardian — Data Center Night Shift Monitoring Kit

> **Replaces a $48,000/year night shift operator with a $76 open hardware sensor kit.**

---

## What It Does

The DC Guardian monitors your data center 24/7 during unstaffed hours (nights, weekends, holidays) and alerts you to:

- 🌡️ **Temperature anomalies** — Detects cooling failures via inlet/exhaust differential
- 💧 **Water leaks** — Catches flooding from cooling units before it damages equipment
- 🔥 **Smoke/Fire** — Early warning for electrical fires before suppression triggers
- 📊 **Humidity spikes** — Prevents condensation damage to servers

All processing happens on the LicheeRV-Nano edge board using PicClaw AI — no cloud subscription required.

## ROI Calculation

| | Human Operator | DC Guardian Kit |
|---|---|---|
| **Annual Cost** | $48,000 (salary + benefits) | $76 (one-time) + ~$5/yr electricity |
| **Coverage** | 8 hrs/night, 5 nights/week | 24/7/365 |
| **Response Time** | Minutes (if awake) | Seconds (automated) |
| **False Negatives** | Fatigue, distraction | Continuous monitoring |
| **Break-even** | — | **0.6 days** |

## Kit Contents

See [BOM.md](BOM.md) for the complete bill of materials with purchase links.

| Component | Purpose |
|-----------|---------|
| LicheeRV-Nano | Edge AI compute board |
| DHT22 ×2 | Temperature + humidity (inlet & exhaust) |
| MQ-2 | Smoke and combustible gas detection |
| Water leak sensors ×2 | Floor and cooling unit flood detection |
| Buzzer + LEDs | Local audible/visual alarm |
| Breadboard + wires | Prototyping connections |
| Enclosure | Protection and mounting |

## Wiring

See [WIRING.md](WIRING.md) for the complete wiring diagram and connection guide.

**Quick summary:**
- DHT22 #1 → PD18 (rack inlet)
- DHT22 #2 → PD16 (rack exhaust)
- MQ-2 → PD12 (digital) / PD14 (analog)
- Water #1 → PD10 (floor)
- Water #2 → PD8 (cooling unit)
- Buzzer → PD6 (via NPN transistor)
- Red LED → PD4 (alarm)
- Green LED → PD2 (status)

## PicClaw Skill Configuration

```yaml
# skill.yaml — DC Guardian
name: dc-guardian
version: 1.0.0
description: Data center night shift monitoring

sensors:
  - id: dht22_inlet
    type: dht22
    pin: PD18
    role: inlet_temp_humidity
    sample_interval: 30s

  - id: dht22_exhaust
    type: dht22
    pin: PD16
    role: exhaust_temp_humidity
    sample_interval: 30s

  - id: mq2_smoke
    type: mq2
    pin_digital: PD12
    pin_analog: PD14
    role: smoke_gas_detection
    sample_interval: 10s
    burn_in_time: 48h

  - id: water_floor
    type: water_leak
    pin: PD10
    role: floor_flood
    sample_interval: 5s

  - id: water_cooling
    type: water_leak
    pin: PD8
    role: cooling_unit_leak
    sample_interval: 5s

actuators:
  - id: buzzer
    type: piezo
    pin: PD6
    role: local_alarm

  - id: led_alarm
    type: led
    pin: PD4
    color: red
    role: alarm_indicator

  - id: led_status
    type: led
    pin: PD2
    color: green
    role: system_ok
```

## Alert Thresholds

```yaml
# alerts.yaml
alerts:
  temperature:
    warning: 30°C      # Above normal
    critical: 35°C     # Server damage risk
    delta_t: 15°C      # Inlet-exhaust differential too high
    cooldown: 300s     # Don't re-alert within 5 minutes

  humidity:
    warning: 60%       # Condensation risk
    critical: 75%      # Immediate action required

  smoke:
    critical: ANY      # Any smoke detection is critical
    auto_alarm: true   # Sound buzzer immediately

  water:
    critical: ANY      # Any water detection is critical
    auto_alarm: true   # Sound buzzer immediately

escalation:
  - level: warning
    channels: [dashboard, telegram]
    delay: 0s

  - level: critical
    channels: [dashboard, telegram, sms, phone_call]
    delay: 0s
    auto_alarm: true
```

## Assembly Steps

1. **Order parts** from the [BOM](BOM.md)
2. **Wire the sensors** following the [Wiring Guide](WIRING.md)
3. **Flash PicClaw** onto the LicheeRV-Nano:
   ```bash
   picclaw flash --board licheerv-nano --firmware dc-guardian
   ```
4. **Install the skill:**
   ```bash
   picclaw skill install dc-guardian
   ```
5. **Run self-test:**
   ```bash
   picclaw test dc-guardian --self-test
   ```
6. **Deploy** to your data center rack
7. **Configure alerts** — Edit `alerts.yaml` with your notification preferences

## Drivers

Sensor driver code is in the `drivers/` directory:

| File | Sensor | Description |
|------|--------|-------------|
| `drivers/dht22.py` | DHT22 | Temperature + humidity reading |
| `drivers/mq2_smoke.py` | MQ-2 | Smoke/gas detection with calibration |
| `drivers/water_leak.py` | Water probe | Flood detection with debounce |

## Grafana Dashboard

Import `dashboard.json` into Grafana for real-time visualization:
- Temperature differential (inlet vs exhaust)
- Humidity trends
- Smoke sensor readings
- Water leak status
- Alert history

## License

[CERN Open Hardware Licence Version 2 — Strongly Reciprocal (CERN-OHL-S-2.0)](../LICENSE)
