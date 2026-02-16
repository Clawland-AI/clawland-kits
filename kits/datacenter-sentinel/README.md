# Datacenter Sentinel Kit

**Replace a $48,000/year night shift operator with an $88 sensor kit and a PicClaw agent.**

<div align="center">

| Metric | Value |
|--------|-------|
| **Total Cost** | ~$88 USD |
| **Annual Replacement Value** | $48,000/yr |
| **ROI Period** | 17 hours |
| **Sensors** | Temperature, Humidity, Smoke, Water Leak |
| **Board** | LicheeRV-Nano (or Raspberry Pi Zero 2 W) |
| **Power** | 5V USB-C (2.5W typical) |

</div>

---

## 💡 Use Case

### The Problem

Datacenters require 24/7 monitoring for:
- 🌡️ **Overheating** — Cooling failure can destroy hardware in minutes
- 💧 **Water leaks** — Burst pipes or A/C condensation cause downtime
- 🔥 **Smoke/fire** — Early detection saves equipment and prevents total loss
- 💨 **Humidity** — Too high = condensation; too low = static discharge

Traditional solution: **$48K/year night shift operator** who walks the aisles every hour.

### The Solution

**Datacenter Sentinel** monitors 24/7 and alerts on anomalies:
- PicClaw agent reads sensors every 5 minutes
- Sends Telegram/Discord alerts on threshold breach
- Escalates to MoltClaw (cloud) if critical
- Logs data to InfluxDB for trend analysis

**Cost**: $88 one-time hardware + $0 ongoing (self-hosted)

---

## 📦 Bill of Materials (BOM)

### Core Components

| Component | Spec | Qty | Price (USD) | Supplier | Link |
|-----------|------|-----|-------------|----------|------|
| **SBC** | LicheeRV-Nano (SG2002, 256MB RAM) | 1 | $17.90 | Sipeed | [Aliexpress](https://www.aliexpress.com/item/1005007394149933.html) |
| Alt: SBC | Raspberry Pi Zero 2 W (RP3A0, 512MB) | 1 | $15.00 | Adafruit | [Buy](https://www.adafruit.com/product/5291) |
| **Temperature/Humidity** | DHT22 (AM2302) Digital Sensor | 1 | $4.95 | Adafruit | [Buy](https://www.adafruit.com/product/385) |
| **Smoke Detector** | MQ-2 Smoke/Gas Sensor Module | 1 | $3.49 | Amazon | [Buy](https://www.amazon.com/dp/B07R9K5R7Z) |
| **Water Leak** | Water Level Detection Sensor | 2 | $1.99 ea | Amazon | [Buy](https://www.amazon.com/dp/B07THDH7Y4) |
| **MicroSD Card** | 32GB Class 10 | 1 | $6.99 | Amazon | [Buy](https://www.amazon.com/dp/B08TJRVWV1) |
| **USB-C Power** | 5V 3A Power Supply | 1 | $7.99 | Amazon | [Buy](https://www.amazon.com/dp/B07TYQRXTK) |
| **Case** | 3D-printed enclosure (optional) | 1 | $0-$8 | — | See design files |

### Wiring & Connectors

| Component | Spec | Qty | Price (USD) | Supplier | Link |
|-----------|------|-----|-------------|----------|------|
| **Jumper Wires** | Female-to-Female, 40-pin set | 1 | $5.99 | Amazon | [Buy](https://www.amazon.com/dp/B077NH83CJ) |
| **Breadboard** | 400-point (for prototyping) | 1 | $4.99 | Amazon | [Buy](https://www.amazon.com/dp/B082KBF7MM) |
| **Screw Terminals** | 2-pin 5mm pitch (for water sensors) | 2 | $0.50 ea | Amazon | [Buy](https://www.amazon.com/dp/B07BS126FK) |
| **Resistor** | 10kΩ pull-up (for DHT22) | 1 | $0.10 | DigiKey | [Buy](https://www.digikey.com/en/products/detail/yageo/CFR-25JB-52-10K/12697) |
| **Heat Shrink Tubing** | 3mm assortment (optional) | 1m | $2.99 | Amazon | [Buy](https://www.amazon.com/dp/B084GDLSCK) |

### Optional Add-ons

| Component | Purpose | Price (USD) | Link |
|-----------|---------|-------------|------|
| **Alarm Buzzer** | Local audible alert | $2.49 | [Adafruit](https://www.adafruit.com/product/1536) |
| **LED Indicator** | Status light (red/green) | $0.50 | [DigiKey](https://www.digikey.com/en/products/detail/qt-brightek/QTB-TWIN5mm/2618030) |
| **4G LTE Module** | Cellular backup (SIM7600G) | $39.99 | [Amazon](https://www.amazon.com/dp/B08R9YZLVV) |
| **Battery Pack** | UPS (10,000mAh, ~40h runtime) | $18.99 | [Amazon](https://www.amazon.com/dp/B07QXV6N1B) |

---

## 💰 Cost Breakdown

### Base Configuration (Minimum)
```
LicheeRV-Nano:     $17.90
DHT22:              $4.95
MQ-2 Smoke:         $3.49
Water Sensors (×2): $3.98
MicroSD Card:       $6.99
USB-C Power:        $7.99
Jumper Wires:       $5.99
Breadboard:         $4.99
Resistor + misc:    $0.50
───────────────────────────
Total:             $56.78
```

### Recommended Configuration
```
Base:              $56.78
Alarm Buzzer:       $2.49
LED Indicators:     $1.00
Screw Terminals:    $1.00
Heat Shrink:        $2.99
3D-printed Case:    $8.00
───────────────────────────
Total:             $72.26
```

### Enterprise Configuration (with backup)
```
Recommended:       $72.26
4G LTE Module:     $39.99
Battery Pack:      $18.99
───────────────────────────
Total:            $131.24
```

**Target: $88 kit** = Base + selected optional components

---

## 🔌 Wiring Diagram

### Pin Assignment (LicheeRV-Nano GPIO)

| Sensor | Pin | GPIO | Function | Notes |
|--------|-----|------|----------|-------|
| DHT22 | Data | GPIO17 | 1-Wire Data | Needs 10kΩ pull-up to 3.3V |
| MQ-2 | Digital Out | GPIO22 | Smoke Detect | HIGH = smoke detected |
| MQ-2 | Analog Out | ADC0 | Gas Level (optional) | For threshold tuning |
| Water #1 | Digital Out | GPIO23 | Leak Detect (Floor) | HIGH = water detected |
| Water #2 | Digital Out | GPIO24 | Leak Detect (Ceiling) | HIGH = water detected |
| Buzzer | Signal | GPIO25 | PWM Output | Optional local alarm |
| LED (Status) | Anode | GPIO26 | Digital Out | Optional status indicator |

### Power Distribution

```
USB-C 5V Power Supply (3A)
    │
    ├─→ LicheeRV-Nano (5V input, onboard regulator → 3.3V logic)
    │
    ├─→ DHT22 (VCC: 3.3V, GND)
    ├─→ MQ-2 (VCC: 5V, GND) — Needs 5V for heater element
    ├─→ Water Sensor #1 (VCC: 3.3V, GND)
    └─→ Water Sensor #2 (VCC: 3.3V, GND)
```

### ASCII Wiring Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      LicheeRV-Nano SBC                           │
│                                                                  │
│  3.3V ●───┬────────────────────┬──────────────┬───────────────┐ │
│           │                    │              │               │ │
│  GND  ●───┼────────┬───────────┼──────────────┼───────────┬───┼─┤
│           │        │           │              │           │   │ │
│  GPIO17 ●─┼────────┼───────────┼──> DHT22     │           │   │ │
│           │     10kΩ           │   (Data)     │           │   │ │
│           └────╱╲╱╲╲───────────┘              │           │   │ │
│                Pull-up                         │           │   │ │
│  GPIO22 ●─────────────────────────────────────┼───────────┼───┤ │
│                                                │           │   │ │
│  GPIO23 ●──> Water Sensor #1 (Digital Out)    │           │   │ │
│  GPIO24 ●──> Water Sensor #2 (Digital Out)    │           │   │ │
│  GPIO25 ●──> Buzzer (PWM, optional)           │           │   │ │
│  GPIO26 ●──> LED Status (optional)            │           │   │ │
│                                                │           │   │ │
│  5V   ●────────────────────────────────────────┼───────────┘   │ │
└──────────────────────────────────────────────────────────────────┘
         │                    │              │
         │                    │              │
     ┌───▼───┐          ┌─────▼────┐   ┌────▼────┐
     │ DHT22 │          │   MQ-2   │   │ Water#1 │
     │  AM   │          │  Smoke   │   │  Leak   │
     │ 2302  │          │  Sensor  │   │ Sensor  │
     └───────┘          └──────────┘   └─────────┘
   (Temp/Humidity)     (Gas/Smoke)     (H2O Detect)
   
       Pin 1: VCC (3.3V)      VCC: 5V         VCC: 3.3V
       Pin 2: Data (GPIO17)   D0: GPIO22      D0: GPIO23
       Pin 3: NC              A0: ADC0        
       Pin 4: GND             GND             GND
```

### Raspberry Pi Zero 2 W Alternative

If using Pi Zero 2 W instead of LicheeRV-Nano:

| Sensor | Pi GPIO | BCM Pin | Physical Pin |
|--------|---------|---------|--------------|
| DHT22 Data | GPIO4 | 4 | Pin 7 |
| MQ-2 Digital | GPIO17 | 17 | Pin 11 |
| Water #1 | GPIO27 | 27 | Pin 13 |
| Water #2 | GPIO22 | 22 | Pin 15 |
| Buzzer | GPIO18 | 18 | Pin 12 (PWM) |

---

## 🛠️ Assembly Instructions

### Step 1: Prepare the Board

1. **Flash PicClaw image** to microSD card:
   ```bash
   # Download pre-built image
   wget https://downloads.clawland.ai/picclaw-licheerv-nano-latest.img.xz
   
   # Flash to SD card (replace /dev/sdX with your SD device)
   xzcat picclaw-licheerv-nano-latest.img.xz | sudo dd of=/dev/sdX bs=4M status=progress
   sync
   ```

2. **Insert microSD** into LicheeRV-Nano
3. **Connect USB-C power** (do not power on yet)

### Step 2: Wire the DHT22 (Temperature/Humidity)

1. **Identify pins** on DHT22:
   - Pin 1 (left): VCC
   - Pin 2: Data
   - Pin 3: NC (not connected)
   - Pin 4 (right): GND

2. **Connect wires**:
   - DHT22 Pin 1 → LicheeRV 3.3V
   - DHT22 Pin 2 → GPIO17
   - DHT22 Pin 4 → GND

3. **Add pull-up resistor**:
   - Solder or breadboard: 10kΩ resistor between Data (GPIO17) and 3.3V
   - This resistor is **critical** for DHT22 operation

### Step 3: Wire the MQ-2 (Smoke Sensor)

1. **MQ-2 module pins** (4-pin version):
   - VCC → 5V (MQ-2 needs 5V for heating element)
   - GND → GND
   - D0 (Digital Out) → GPIO22
   - A0 (Analog Out) → Optional (ADC0 if you want analog reading)

2. **Calibration**:
   - MQ-2 has a potentiometer (blue screw) for threshold adjustment
   - Turn clockwise to increase sensitivity
   - Start at mid-position, tune after testing

### Step 4: Wire Water Leak Sensors

1. **Water Sensor #1** (Floor sensor):
   - VCC → 3.3V
   - GND → GND
   - D0 → GPIO23

2. **Water Sensor #2** (Ceiling/pipe sensor):
   - VCC → 3.3V
   - GND → GND
   - D0 → GPIO24

3. **Mounting tips**:
   - Floor sensor: Place under raised floor tiles near A/C units
   - Ceiling sensor: Attach near overhead pipes with double-sided tape

### Step 5: Optional Components

#### Alarm Buzzer
- Positive → GPIO25
- Negative → GND
- Configure as PWM output (see skill config)

#### Status LED
- Anode (long leg) → GPIO26 via 220Ω resistor
- Cathode (short leg) → GND
- Green = normal, Red = alert

### Step 6: Final Assembly

1. **Use breadboard for prototyping**, then transfer to:
   - Perfboard (solder for permanent install)
   - Or use screw terminals for modular design

2. **Cable management**:
   - Use zip ties or velcro straps
   - Label each sensor cable ("DHT22", "MQ-2", "Water-1", "Water-2")
   - Leave ~1m slack for repositioning

3. **Enclosure** (optional):
   - 3D-print case from `enclosure/datacenter-sentinel.stl`
   - Or use off-the-shelf project box (recommend vented for MQ-2 heater)

---

## 📸 Assembly Photos

_Photos to be added:_
- [ ] Step-by-step wiring process
- [ ] Completed breadboard prototype
- [ ] Installed in datacenter environment
- [ ] 3D-printed enclosure (if available)

**Community contributions welcome!** Submit photos via PR or GitHub Issues.

---

## ⚙️ PicClaw Configuration

### Install the Skill

```bash
# SSH into PicClaw device
ssh picclaw@licheerv-nano.local

# Install datacenter-sentinel skill
picclaw skill install datacenter-sentinel
```

### Configure Thresholds

Edit `/etc/picclaw/skills/datacenter-sentinel/config.yaml`:

```yaml
sensors:
  dht22:
    gpio_pin: 17
    read_interval: 300  # seconds (5 minutes)
    thresholds:
      temp_warning: 28.0   # °C
      temp_critical: 35.0
      humidity_warning_low: 30.0   # %
      humidity_warning_high: 70.0
      humidity_critical_high: 85.0
  
  mq2_smoke:
    gpio_pin: 22
    mode: digital  # or "analog" if using ADC
    threshold: HIGH  # Trigger on HIGH signal
    debounce_ms: 2000
  
  water_leak:
    floor_sensor:
      gpio_pin: 23
      threshold: HIGH
    ceiling_sensor:
      gpio_pin: 24
      threshold: HIGH
    debounce_ms: 1000

alerts:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
  
  discord:
    enabled: false
    webhook_url: ""
  
  local_alarm:
    buzzer_gpio: 25
    enabled: true
    duration_seconds: 10
  
  escalation:
    moltclaw_url: "https://your-moltclaw-cloud.example.com"
    enabled: true
    on_critical_only: true

logging:
  influxdb:
    enabled: false
    url: "http://influxdb.local:8086"
    database: "datacenter_sensors"
  
  local_csv:
    enabled: true
    path: "/var/log/picclaw/datacenter_sensors.csv"
    rotate_daily: true
```

### Test the Installation

```bash
# Manual sensor test
picclaw skill run datacenter-sentinel check

# View live readings
picclaw skill run datacenter-sentinel monitor

# Test alert system (sends test notification)
picclaw skill run datacenter-sentinel test-alert
```

---

## 📊 ROI Calculation

### Traditional Solution
```
Night shift operator salary:  $48,000/year
Benefits (30%):               $14,400/year
Training/onboarding:           $5,000 one-time
───────────────────────────────────────────
Annual cost:                  $62,400/year
```

### Datacenter Sentinel Solution
```
Hardware (one-time):               $88
PicClaw license:                   $0 (open source)
Power (2.5W × $0.12/kWh × 8760h): $2.63/year
Maintenance:                      $0 (self-hosted)
───────────────────────────────────────────
First year cost:                  $90.63
Subsequent years:                  $2.63/year
```

### Savings
```
Year 1:  $62,400 - $90.63  = $62,309 saved
Year 2+: $62,400 - $2.63   = $62,397/year saved

ROI period: ($88 / $62,400/year) × 365 days = 0.51 days = 12.3 hours
```

**Payback in half a day.** The kit pays for itself before your operator's first shift ends.

---

## 🧪 Testing & Validation

### Sensor Verification

1. **DHT22 (Temperature/Humidity)**:
   ```bash
   # Read current values
   picclaw sensor read dht22
   
   # Expected: temp=20-25°C, humidity=40-60%
   # If zeros: check wiring, pull-up resistor
   ```

2. **MQ-2 (Smoke)**:
   ```bash
   # Baseline (clean air)
   picclaw sensor read mq2
   # Should show LOW or low analog value
   
   # Test: light a match 30cm away
   # Should trigger within 5-10 seconds
   ```

3. **Water Leak**:
   ```bash
   # Dry test
   picclaw sensor read water
   # Both sensors: LOW
   
   # Wet test: touch sensor pads with damp cloth
   # Should show HIGH within 1 second
   ```

### Alert Testing

```bash
# Simulate temperature alert
picclaw skill run datacenter-sentinel simulate --temp=40

# Simulate water leak
picclaw skill run datacenter-sentinel simulate --water-floor=true

# Full system test
picclaw skill run datacenter-sentinel test-all
```

---

## 🚨 Common Issues & Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| DHT22 reads all zeros | Missing pull-up resistor | Add 10kΩ resistor between Data and 3.3V |
| MQ-2 always triggers | Sensor not warmed up | Wait 2-3 minutes after power on |
| Water sensor false positives | Corrosion on pads | Clean with isopropyl alcohol |
| No Telegram alerts | Wrong bot token/chat ID | Verify credentials with `curl` test |
| PicClaw won't boot | Corrupt SD card image | Re-flash image, use quality SD card |

---

## 📖 Further Reading

- [PicClaw Documentation](https://clawland.ai/docs/picclaw)
- [Sensor Driver Reference](https://clawland.ai/docs/drivers)
- [Skill Development Guide](https://clawland.ai/docs/skills)
- [Contributor Revenue Share](https://github.com/Clawland-AI/.github/blob/main/CONTRIBUTOR-REVENUE-SHARE.md)

---

## 🤝 Contributing

Found a better sensor? Improved the wiring? Took photos?

1. Fork this repository
2. Add your improvements
3. Submit a Pull Request
4. Earn points in the Clawland Revenue Pool

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

---

## 📜 License

**CERN Open Hardware Licence Version 2 — Strongly Reciprocal (CERN-OHL-S-2.0)**

All hardware designs, schematics, and BOMs in this kit are open hardware. See [LICENSE](../../LICENSE) for full terms.

---

**Built by the Clawland community** 🍇  
_Making industrial monitoring accessible to everyone._
